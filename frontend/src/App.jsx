import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import io from "socket.io-client"
function App() {
  const [count, setCount] = useState(0);
  const [seconds, setSeconds] = useState(0);
  const [socket, setSocket] = useState(null);
  const [sid, setSid] = useState(null)


  useEffect(() => {
    const socketInstance = io('http://localhost:5000', {
      transports: ["websocket"],
      cors: {
        origin: "http://localhost:5000/",
        withCredentials: true,
      }
    });
    setSocket(socketInstance);

    socketInstance.on('connect', () => {
      console.log('Connected to server');
      // socketInstance.emit('login', "ll")
    });
    socketInstance.on("client_sid", (data) => {
      console.log(data);
      setSid(data);
    })

    socketInstance.on('message', (data) => {
      console.log(`Received message: ${data}`);
    });

    socketInstance.on('completed', (data) => {
      alert("Task is completed ");
      console.log("Task is completed ");
    })
    // return () => {
    //   if (socketInstance) {
    //     socketInstance.disconnect();
    //   }
    // };

  }, [])

  const handleSecondsNumber = (e) => {
    e.preventDefault();
    setSeconds(e.target.value);
  }

  const make_task_request = async (e) => {
    const req = await fetch(`http://localhost:5000/launch_task/${seconds}/${sid}`, { method: 'POST' });
    if (req.ok) {
      alert(await req.text());
    }
  }
  return (
    <>
      <input onChange={handleSecondsNumber} type="number" name="seconds" min='0' className="seconds" />
      <button onClick={make_task_request}> Send tasks</button>
    </>
  )
}

export default App
