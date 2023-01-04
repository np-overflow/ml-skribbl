<script lang="ts">
  import { browser } from "$app/environment";
  import { onMount } from "svelte";
  import "iconify-icon";

  var time = 30;
  var timer: NodeJS.Timer;
  var category: string;

  const clearCanvas = () => {
    const canvas = document.getElementById("board") as HTMLCanvasElement,
      context = canvas.getContext("2d");
    if (context) {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
  };

  const convertBlobToDataURL = (blob: Blob) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onerror = reject;
      reader.onload = () => {
        resolve(reader.result);
      };
      reader.readAsDataURL(blob);
    });
  };

  const predictImage = async (canvas: HTMLCanvasElement) => {
    const imageContent = canvas.toDataURL("image/png");
    const resizedImage = await fetch("http://localhost:5000/transform", {
      method: "POST",
      body: imageContent
    }).then(async (response) => {
      const blob = await response.blob();
      const dataURL = (await convertBlobToDataURL(blob)) as string;
      return dataURL;
    });

    const predictions = await fetch("http://localhost:5000/predict", {
      method: "POST",
      body: resizedImage
    }).then((response) => response.text());

    const modelMessage = document.querySelector("#panel__model");
    const startingModelMessage = document.querySelector("#panel__model__start");
    if (modelMessage) {
      startingModelMessage?.remove();
      const choices = [
        "Looks like ",
        "I think it's ",
        "I'm guessing it's ",
        "I'm pretty sure it's "
      ];
      const article = predictions.match(/^[AEIOU]/i) ? "an" : "a";
      const guessElement = document.createElement("p");
      guessElement.innerHTML =
        choices[Math.floor(Math.random() * choices.length)] + article + " " + predictions + "!";

      modelMessage.insertBefore(guessElement, modelMessage.childNodes[1]);
    }

    if (predictions === category) {
      endGame(Condition.WIN);
      clearInterval(timer);
    }
  };

  enum Condition {
    WIN,
    LOSE
  }

  const endGame = (condition: Condition) => {
    clearInterval(timer);
    const serverMessage = document.querySelector("#panel__server p");
    const modelMessage = document.querySelector("#panel__model p");
    if (condition === Condition.WIN) {
      if (serverMessage && modelMessage) {
        serverMessage.innerHTML = "Awesome! Starting new game soon...";
        modelMessage.innerHTML = "Great! It took me " + (30 - time) + " seconds to guess it!";
      }
    } else {
      if (serverMessage) {
        serverMessage.innerHTML = "Good attempt! Starting new game soon...";
      }
    }

    clearCanvas();

    const pause = setTimeout(() => {
      startGame();
      clearTimeout(pause);
      const modelPanel = document.querySelector("#panel__model");
      if (modelPanel) {
        const pTags = modelPanel.querySelectorAll("p");
        pTags.forEach((p) => p.remove());
      }
    }, 3000);
  };

  const startGame = async () => {
    time = 30;
    const modelMessage = document.querySelector("#panel__model p");
    const serverMessage = document.querySelector("#panel__server p");
    const headerMessage = document.querySelector(".heading > h1");
    if (modelMessage) {
      modelMessage.remove();
    }
    if (serverMessage) {
      serverMessage.innerHTML = "Thinking of something for you to draw...";
    }

    category = await fetch("http://localhost:5000/start", {
      method: "GET"
    }).then((response) => {
      timer = setInterval(() => {
        if (time > 0 && headerMessage) {
          time--;
          headerMessage.innerHTML = "Draw away! " + time + " seconds left";
        } else {
          endGame(Condition.LOSE);
          clearInterval(timer);
        }
      }, 1000);
      return response.text();
    });

    if (serverMessage) {
      const article = category.match(/^[AEIOU]/i) ? "an" : "a";
      serverMessage.innerHTML = "Draw " + article + " " + category + "!";
    }
  };

  onMount(() => {
    if (browser) {
      const canvas = document.getElementById("board") as HTMLCanvasElement,
        context = canvas.getContext("2d");
      var isDrawing = false;

      canvas.height = canvas.offsetHeight;
      canvas.width = canvas.offsetWidth;
      startGame();

      if (context) {
        const draw = (e: MouseEvent | TouchEvent) => {
          if (!isDrawing) return;
          context.lineWidth = 5;
          context.lineCap = "round";
          context.strokeStyle = "black";

          var x, y;
          if (e instanceof MouseEvent) {
            x = e.offsetX;
            y = e.offsetY;
          } else {
            x = e.touches[0].clientX - canvas.offsetLeft;
            y = e.touches[0].clientY - canvas.offsetTop;
          }
          context.lineTo(x, y);
          context.stroke();
        };

        canvas.addEventListener("mousemove", (e) => draw(e));
        canvas.addEventListener("touchmove", (e) => draw(e));

        canvas.addEventListener("mousedown", () => {
          if (time > 0) {
            isDrawing = true;
            context.beginPath();
          }
        });
        canvas.addEventListener("touchstart", () => {
          if (time > 0) {
            isDrawing = true;
            context.beginPath();
          }
        });

        canvas.addEventListener("mouseup", () => {
          if (time > 0) {
            isDrawing = false;
            predictImage(canvas);
          }
        });
        canvas.addEventListener("touchend", () => {
          if (time > 0) {
            isDrawing = false;
            predictImage(canvas);
          }
        });
      }
    }
  });
</script>

<main>
  <section>
    <div id="canvas">
      <div class="heading">
        <iconify-icon icon="material-symbols:draw-rounded" style="font-size: 2em;" />
        <h1>Draw away! {time} seconds left</h1>
      </div>
      <canvas id="board" />
      <button on:click={() => clearCanvas()}>Clear board</button>
      <button
        on:click={() => {
          time = 0;
          endGame(Condition.LOSE);
        }}>Skip round</button
      >
    </div>
    <div id="panel">
      <div id="panel__server">
        <h2>Server</h2>
        <p>The game hasn't started yet. Give me a moment!</p>
      </div>
      <div id="panel__model">
        <h2>Model</h2>
        <p id="panel__model__start">Hurry up already...</p>
      </div>
    </div>
  </section>
</main>

<div id="background" />

<style>
  :global(*) {
    margin: 0;
  }

  :global(html, body) {
    overflow: hidden;
  }

  #background,
  main {
    height: 100vh;
    width: 100vw;
  }

  #background {
    position: absolute;
    top: 0;
    background: linear-gradient(#ff8e2c, #ff5a81);
  }

  main {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  section {
    min-height: 75%;
    min-width: 75%;
    z-index: 1;
    background-color: white;
    border-radius: 1rem;
    display: flex;
    flex-direction: column;
    padding: 2em;
    gap: 2em;
  }

  @media screen and (min-width: 768px) {
    section {
      flex-direction: row;
    }

    #canvas {
      height: auto;
      flex: 1.75;
    }
  }

  section > div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1em;
    min-width: fit-content;
  }

  #canvas {
    height: fit-content;
  }

  #panel {
    flex: 1.25;
  }

  canvas {
    aspect-ratio: 1/1;
    border-radius: 0.5rem;
    border: 1px solid #ccc;
  }

  .heading > * {
    display: inline-block;
    vertical-align: middle;
  }

  #panel {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 2.5em;
  }

  #panel div {
    padding: 2em 1em 1em 1em;
    border-radius: 0.5rem;
    position: relative;
  }

  #panel div h2 {
    position: absolute;
    top: -18px;
    left: 0;
    padding: 0 0.25em;
    border-radius: 0.5rem;
  }

  #panel__server {
    background-color: #ffe3ca;
    flex: 1;
  }

  #panel__server h2 {
    background-color: #ff8e2c;
    color: white;
  }

  #panel__model {
    border: 2px dotted #ccc;
    flex: 3;
  }

  #panel__model h2 {
    background-color: white;
    color: #ccc;
  }

  button {
    appearance: none;
    border: none;
    background-color: #eee;
    padding: 0.75em;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: background-color 0.1s ease;
  }

  button:hover {
    background-color: #ddd;
  }
</style>
