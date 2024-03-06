import "./App.css";
import { useEffect, useRef, useState } from "react";
import emojis from "./emojis.js";
import config from "./config.js";

function App() {
    const canvasRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [emoji, setEmoji] = useState({});
    const [message, setMessage] = useState('');
    const setRandomEmoji = () => {
        const name =
            Object.keys(emojis)[
                Math.floor(Math.random() * Object.keys(emojis).length)
            ];
        setEmoji({
            name,
            emoji: emojis[name],
        });
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        setRandomEmoji();
    }, []);

    const startDrawing = (event) => {
        const { offsetX, offsetY } = getCoordinates(event);
        const ctx = canvasRef.current.getContext("2d");
        ctx.beginPath();
        ctx.moveTo(offsetX, offsetY);
        setIsDrawing(true);
    };

    const draw = (event) => {
        if (!isDrawing) return;
        const { offsetX, offsetY } = getCoordinates(event);
        const ctx = canvasRef.current.getContext("2d");
        ctx.lineTo(offsetX, offsetY);
        ctx.stroke();
    };

    const endDrawing = () => {
        setIsDrawing(false);
    };

    const getCoordinates = (event) => {
        if (event.nativeEvent instanceof MouseEvent) {
            return {
                offsetX: event.nativeEvent.offsetX,
                offsetY: event.nativeEvent.offsetY,
            };
        } else {
            const rect = canvasRef.current.getBoundingClientRect();
            return {
                offsetX: event.nativeEvent.touches[0].clientX - rect.left,
                offsetY: event.nativeEvent.touches[0].clientY - rect.top,
            };
        }
    };

    const handleSubmit = () => {
        const canvas = canvasRef.current;
        canvas.toBlob((blob) => {
            const formData = new FormData();
            formData.append("file", blob, "drawing.png");
            fetch(`${config.BACKEND_URL}/upload/${emoji.name}`, {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => console.log(data))
                .catch((error) => console.error(error));

            fetch(`${config.BACKEND_URL}/send/${emoji.name}`, {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => console.log(data))
                .catch((error) => console.error(error));
        });
        handleClear();
        setRandomEmoji();
    };

    const handleClear = () => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    };

    const handleSkip = () => {
        handleClear();
        setRandomEmoji();
    }

    useEffect(() => {
        setRandomEmoji();
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            canvasRef.current.toBlob((blob) => {
                const formData = new FormData();
                console.log(emoji.name);
                formData.append("file", blob, "drawing.png");
                fetch(`${config.BACKEND_URL}/send/${emoji.name}`, {
                    method: "POST",
                    body: formData,
                })
                    .then((response) => response.json())
                    .then((data) => {
                        setMessage(data.message)
                        console.log(data.message)
                        console.log(data)
                    })
                    .catch((error) => console.error(error));
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [emoji.name]);


    return (
        <>
            <h3>
                Draw {emoji.name}: {emoji.emoji}
            </h3>
            <canvas
                ref={canvasRef}
                width={256}
                height={256}
                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={endDrawing}
                onMouseOut={endDrawing}
                onTouchStart={startDrawing}
                onTouchMove={draw}
                onTouchEnd={endDrawing}
                style={{ border: "1px solid black" }}
            />
            <br />
            <button onClick={handleSubmit}>Submit</button>
            <span> </span>
            <button onClick={handleClear}>Clear</button>
            <span> </span>
            <button onClick={handleSkip}>Skip</button>
            <div id = "output">{message}</div>
        </>
    );
}

export default App;
