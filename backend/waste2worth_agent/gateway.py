class BuyerCommunicationGateway:
    def send_waste_offer(self, buyer_id, payload):
        raise NotImplementedError

    def get_buyer_response(self, conversation_id):
        raise NotImplementedError


class TransactionGateway:
    def update_transaction_status(self, transaction_id, status, payload):
        raise NotImplementedError


class EventGateway:
    def record_event(self, transaction_id, event_type, actor, message, payload=None):
        raise NotImplementedError
