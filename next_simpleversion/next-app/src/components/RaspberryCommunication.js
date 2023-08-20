import { useState } from 'react'; // Remove useClient import
import axios from 'axios';

const RaspberryCommunication = () => {
  const [receivedData, setReceivedData] = useState(null);
  const [sentData, setSentData] = useState('');

  const fetchData = async () => {
    try {
      const response = await axios.get('http://192.168.8.125:5000/get_data');
      setReceivedData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const sendData = async () => {
    try {
      await axios.post('http://192.168.8.125:5000/send_data', { data: sentData });
      setSentData('');
      fetchData();
    } catch (error) {
      console.error('Error sending data:', error);
    }
  };

  return (
    <div>
      <div>
        <button onClick={fetchData}>Fetch Data</button>
        <div>Received Data: {JSON.stringify(receivedData)}</div>
      </div>
      <div>
        <input
          type="text"
          value={sentData}
          onChange={(e) => setSentData(e.target.value)}
        />
        <button onClick={sendData}>Send Data</button>
      </div>
    </div>
  );
};

export default RaspberryCommunication;
