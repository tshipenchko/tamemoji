import "./App.css";
import { useEffect, useRef, useState } from "react";

function App() {
    const canvasRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);

    // Initialize canvas context when component mounts
    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
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
            fetch("http://localhost:8000/upload/smile", {
                method: "POST",
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => console.log(data))
                .catch((error) => console.error(error));
        });
    };

    const handleClear = () => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    };

    return (
        <>
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
        </>
    );
}

export default App;
