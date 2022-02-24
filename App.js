// import React and hooks to access state and Lifecycle methods
import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

// endpoint variable
let endPoint = "http://localhost:5000";
// connect with server using socket io
let socket = io.connect(`${endPoint}`);

// functional component
const App = () => {
    // create state using hooks
    const [messages, setMessages] = useState(["Hello and Welcome"]);
    const [message, setMessage] = useState("");

    // componentDidUpdate method as hook (useEffect). this will auto call when message length changes
    useEffect(() => {
        getMessages();
    }, [messages.length]);

    // This method will call when the app renders for the first time and every time message Length changes
    const getMessages = () => {
        socket.on("message", msg => {
            setMessages([...messages, msg]);
        });
        socket.on("connect", msg => {
            alert(msg);
        });
    };

    // On Change input field this will call
    const onChange = e => {
        setMessage(e.target.value);
    };

    // event handler for the "send message" button
    const onClick = () => {
        if (message !== "") {
            socket.emit("message", message);
            setMessage("");
        }
        else {
            alert("Please Add A Message");
        }
    };

    const onClick2 = () => {
        fetch(endPoint)
            .then(response => console.log(response));
    }

    // Return the view
    return (
        <div>
        { messages.length > 0 && messages.map(msg => (
            <div>
                <p>{msg}</p>
            </div>
        ))}
            <input value={message} name="message" onChange={e => onChange(e)} />
            <button onClick={() => onClick()}>Send Message</button>
            <button onClick={() => onClick2()}>Get dummy data</button>
        </div>
    );
};
export default App;
