from waste2worth_agent.messaging import generate_outreach_message, suggest_counter_offer
from waste2worth_agent.negotiation import evaluate_offer
from waste2worth_ai.validation import parse_supplier_rules


class Waste2WorthAgent:
    def __init__(self, communication_gateway, transaction_gateway, event_gateway=None):
        self.communication_gateway = communication_gateway
        self.transaction_gateway = transaction_gateway
        self.event_gateway = event_gateway

    def contact_and_negotiate(
        self,
        transaction_id,
        waste_analysis,
        selected_buyer,
        supplier_rules,
        supplier_approved_contact,
    ):
        events = []
        transcript = []
        rules = parse_supplier_rules(supplier_rules)

        if not supplier_approved_contact:
            self._record_event(
                transaction_id,
                "waiting_for_supplier_approval",
                "ai_agent",
                "Supplier approval required before buyer contact.",
            )
            return {
                "status": "waiting_for_supplier_approval",
                "events": ["waiting_for_supplier_approval"],
                "transcript": transcript,
                "deal": None,
            }

        if not selected_buyer:
            self._record_event(transaction_id, "offer_rejected", "ai_agent", "No selected buyer was provided.")
            return {
                "status": "offer_rejected",
                "events": ["no_selected_buyer"],
                "transcript": transcript,
                "deal": None,
            }

        outreach = generate_outreach_message(waste_analysis, selected_buyer, {
            "minimum_total_price": rules.minimum_total_price,
            "requires_pickup": rules.requires_pickup,
        })

        payload = {
            "waste_type": waste_analysis["display_name"],
            "quantity_kg": waste_analysis["quantity_kg"],
            "condition": waste_analysis["condition"],
            "supplier_expectation": rules.minimum_total_price,
            "pickup_required": rules.requires_pickup,
            "outreach_message": outreach,
        }
        conversation_id = self.communication_gateway.send_waste_offer(
            selected_buyer["buyer_id"],
            payload,
        )
        events.append("buyer_contacted")
        transcript.append({"sender": "ai_agent", "message": outreach["body"], "source": outreach["source"]})
        self._record_event(transaction_id, "buyer_contacted", "ai_agent", "Buyer contacted.", payload)

        offer = self.communication_gateway.get_buyer_response(conversation_id)
        events.append("offer_received")
        transcript.append({"sender": "buyer", "message": offer})
        self._record_event(transaction_id, "offer_received", "buyer", "Buyer response received.", offer)

        if evaluate_offer(offer, rules):
            final_offer = offer
            events.append("buyer_offer_accepted")
            transcript.append(
                {
                    "sender": "ai_agent",
                    "message": "Offer accepted: within supplier limits.",
                    "source": "rule_negotiation",
                }
            )
        elif rules.allow_counter_offer:
            counter_offer = suggest_counter_offer(
                waste_analysis,
                selected_buyer,
                {"minimum_total_price": rules.minimum_total_price, "requires_pickup": rules.requires_pickup},
                latest_offer=offer,
            )
            final_offer = self.communication_gateway.send_waste_offer(
                selected_buyer["buyer_id"],
                {
                    "counter_offer": {
                        "total_price": counter_offer["total_price"],
                        "pickup_included": counter_offer["pickup_included"],
                    },
                    "conversation_id": conversation_id,
                },
            )
            events.append("counter_offer_sent")
            transcript.append(
                {
                    "sender": "ai_agent",
                    "message": f"Counter offer: {counter_offer['total_price']} "
                    f"(pickup {'included' if counter_offer['pickup_included'] else 'not included'}): "
                    f"{counter_offer['rationale']}",
                    "source": counter_offer["source"],
                }
            )
            self._record_event(
                transaction_id,
                "counter_offer_sent",
                "ai_agent",
                "Counter offer sent according to supplier rules.",
                counter_offer,
            )
            if not evaluate_offer(final_offer, rules):
                self.transaction_gateway.update_transaction_status(
                    transaction_id,
                    "offer_rejected",
                    {"offer": final_offer},
                )
                events.append("counter_offer_rejected")
                return {"status": "offer_rejected", "events": events, "transcript": transcript, "deal": None}
            events.append("counter_offer_accepted")
        else:
            self.transaction_gateway.update_transaction_status(
                transaction_id,
                "offer_rejected",
                {"offer": offer},
            )
            return {"status": "offer_rejected", "events": events, "transcript": transcript, "deal": None}

        deal = {
            "buyer_id": selected_buyer["buyer_id"],
            "buyer_name": selected_buyer["name"],
            "final_total_price": final_offer["total_price"],
            "pickup_included": final_offer["pickup_included"],
            "transaction_status": "deal_confirmed",
        }
        self.transaction_gateway.update_transaction_status(transaction_id, "deal_confirmed", deal)
        self._record_event(transaction_id, "deal_confirmed", "ai_agent", "Deal confirmed.", deal)
        events.append("transaction_updated")
        transcript.append({"sender": "ai_agent", "message": "Deal confirmed.", "source": "rule_negotiation"})

        return {"status": "deal_confirmed", "events": events, "transcript": transcript, "deal": deal}

    def _record_event(self, transaction_id, event_type, actor, message, payload=None):
        if self.event_gateway is None:
            return
        self.event_gateway.record_event(transaction_id, event_type, actor, message, payload or {})
