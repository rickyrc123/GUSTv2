import { useState } from "react";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>My test React App!</h1>
      <p style={styles.text}>Click the button to increase the count:</p>
      <button style={styles.button} onClick={() => setCount(count + 1)}>
        Count: {count}
      </button>
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    padding: "50px",
    fontFamily: "Arial, sans-serif",
    backgroundColor: "#282c34",
    color: "white",
    minHeight: "100vh",
  },
  header: {
    fontSize: "2.5rem",
  },
  text: {
    fontSize: "1.2rem",
  },
  button: {
    padding: "10px 20px",
    fontSize: "1.5rem",
    backgroundColor: "#61dafb",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    marginTop: "10px",
  },
};

export default App;
