import pytest
import json
import socket
from unittest.mock import patch, MagicMock
from app.routes import read_sensors


class TestReadSensors:
    """Unit tests for the read_sensors() function"""

    @patch('app.routes.socket.socket')
    def test_read_sensors_success(self, mock_socket_class):
        """Test successful sensor data retrieval"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        
        sensor_data = {"time": "02/20/2026    15:14:52", "temperature": 22.5, "humidity": 45, "pressure": 1013}
        mock_socket_instance.recv.side_effect = [
            json.dumps(sensor_data).encode(),
            b''  # Empty chunk to signal end of stream
        ]
        
        # Act
        result = read_sensors()
        
        # Assert
        assert result == json.dumps(sensor_data)
        mock_socket_instance.connect.assert_called_once_with(("smart-home-mqtt-subscriber", 12345))
        assert mock_socket_instance.recv.call_count == 2

    @patch('app.routes.socket.socket')
    def test_read_sensors_multiple_chunks(self, mock_socket_class):
        """Test sensor data received in multiple chunks"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        chunk1 = b'{"time": "02/20/2026    15:14:52",'
        chunk2 = b'"temperature": 22'
        chunk3 = b'.5, "humidity": 45,'
        chunk4 = b', "pressure": 1013}'
        mock_socket_instance.recv.side_effect = [chunk1, chunk2, chunk3, chunk4, b'']
        
        # Act
        result = read_sensors()
        
        # Assert
        expected = chunk1 + chunk2 + chunk3 + chunk4
        assert result == expected.decode()
        assert mock_socket_instance.recv.call_count == 5

    @patch('app.routes.socket.socket')
    def test_read_sensors_empty_response(self, mock_socket_class):
        """Test handling of empty sensor response"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b''
        
        # Act
        result = read_sensors()
        
        # Assert
        assert result == ''
        mock_socket_instance.connect.assert_called_once()

    @patch('app.routes.socket.socket')
    def test_read_sensors_large_data(self, mock_socket_class):
        """Test handling of large sensor data"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        
        # Create large JSON data
        large_data = {f"sensor_{i}": i * 1.5 for i in range(1000)}
        large_json = json.dumps(large_data).encode()
        
        mock_socket_instance.recv.side_effect = [large_json, b'']
        
        # Act
        result = read_sensors()
        
        # Assert
        assert result == large_json.decode()
        assert len(result) > 5000  # Should be substantial data

    @patch('app.routes.socket.socket')
    def test_read_sensors_special_characters(self, mock_socket_class):
        """Test sensor data with special characters"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        
        sensor_data = {
            "location": "Hallway",
            "description": "Temperature & Humidity Sensor",
            "unit": "°C"
        }
        json_string = json.dumps(sensor_data)
        mock_socket_instance.recv.side_effect = [json_string.encode(), b'']
        
        # Act
        result = read_sensors()
        
        # Assert
        assert result == json_string

    @patch('app.routes.socket.socket')
    def test_read_sensors_connection_called_correctly(self, mock_socket_class):
        """Test that socket connection is made with correct parameters"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.recv.return_value = b''
        
        # Act
        read_sensors()
        
        # Assert
        mock_socket_class.assert_called_once_with(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        mock_socket_instance.connect.assert_called_once_with(
            ("smart-home-mqtt-subscriber", 12345)
        )

    @patch('app.routes.socket.socket')
    def test_read_sensors_connection_error(self, mock_socket_class):
        """Test handling of connection error"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.connect.side_effect = ConnectionRefusedError("Connection refused")
        
        # Act & Assert
        with pytest.raises(ConnectionRefusedError):
            read_sensors()

    @patch('app.routes.socket.socket')
    def test_read_sensors_timeout_error(self, mock_socket_class):
        """Test handling of socket timeout"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        mock_socket_instance.recv.side_effect = TimeoutError("Socket timeout")
        
        # Act & Assert
        with pytest.raises(TimeoutError):
            read_sensors()

    @patch('app.routes.socket.socket')
    def test_read_sensors_numeric_data(self, mock_socket_class):
        """Test sensor data with various numeric formats"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        
        sensor_data = {
            "temperature": 22.5,
            "humidity": 45,
            "pressure": 1013.25,
            "count": 12345,
            "value": -5.75
        }
        mock_socket_instance.recv.side_effect = [
            json.dumps(sensor_data).encode(),
            b''
        ]
        
        # Act
        result = read_sensors()
        
        # Assert
        parsed_result = json.loads(result)
        assert parsed_result == sensor_data

    @patch('app.routes.socket.socket')
    def test_read_sensors_multiple_recv_calls(self, mock_socket_class):
        """Test that socket.recv is called until empty chunk is received"""
        # Arrange
        mock_socket_instance = MagicMock()
        mock_socket_class.return_value.__enter__.return_value = mock_socket_instance
        
        mock_socket_instance.recv.side_effect = [
            b'{"data": ',
            b'"part1"} ',
            b'{"data": ',
            b'"part2"}',
            b''
        ]
        
        # Act
        result = read_sensors()
        
        # Assert
        expected = b'{"data": "part1"} {"data": "part2"}'
        assert result == expected.decode()
        assert mock_socket_instance.recv.call_count == 5
