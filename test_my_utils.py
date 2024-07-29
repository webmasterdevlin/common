import unittest
from unittest.mock import patch, MagicMock
from utils.azure_service_bus import MessageBus


class TestMessageBus(unittest.TestCase):

    @patch('utils.azure_service_bus.ServiceBusClient')
    def test_connect(self, mock_service_bus_client):
        mock_service_bus_client.from_connection_string.return_value = MagicMock()
        bus = MessageBus()
        bus.connect()
        mock_service_bus_client.from_connection_string.assert_called_once_with(bus.connection_str)
        self.assertIsNotNone(bus.servicebus_client)

    @patch('utils.azure_service_bus.ServiceBusClient')
    @patch('utils.azure_service_bus.ServiceBusMessage')
    def test_send(self, mock_service_bus_message, mock_service_bus_client):
        mock_service_bus_client.from_connection_string.return_value.get_queue_sender.return_value.__enter__.return_value = MagicMock()
        bus = MessageBus()
        bus.connect()
        bus.send('test_queue', 'test_message', 'test_correlation_id')
        mock_service_bus_message.assert_called_once_with('test_message', message_id='test_correlation_id')

    @patch('utils.azure_service_bus.ServiceBusClient')
    def test_start_consuming(self, mock_service_bus_client):
        mock_receiver = MagicMock()
        mock_service_bus_client.from_connection_string.return_value.get_queue_receiver.return_value.__enter__.return_value = mock_receiver
        bus = MessageBus()
        bus.connect()
        callback = MagicMock()
        mock_receiver.__iter__.return_value = [MagicMock()]
        bus.start_consuming('test_queue', callback)
        for msg in mock_receiver:
            callback.assert_called_once_with(msg)

    @patch('utils.azure_service_bus.ServiceBusReceiver')
    def test_acknowledge_message(self, mock_service_bus_receiver):
        mock_receiver = MagicMock()
        mock_message = MagicMock()
        bus = MessageBus()
        bus.acknowledge_message(mock_receiver, mock_message)
        mock_receiver.complete_message.assert_called_once_with(mock_message)

    @patch('utils.azure_service_bus.ServiceBusReceiver')
    def test_not_acknowledge_message(self, mock_service_bus_receiver):
        mock_receiver = MagicMock()
        mock_message = MagicMock()
        bus = MessageBus()
        bus.not_acknowledge_message(mock_receiver, mock_message, requeue=True)
        mock_receiver.abandon_message.assert_called_once_with(mock_message)
        bus.not_acknowledge_message(mock_receiver, mock_message, requeue=False)
        mock_receiver.dead_letter_message.assert_called_once_with(mock_message)


if __name__ == '__main__':
    unittest.main()
