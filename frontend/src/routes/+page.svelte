<script lang="ts">
  import { browser } from "$app/environment";
  import { onMount } from "svelte";
  import "iconify-icon";

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

    console.log(resizedImage)

    const predictions = await fetch("http://localhost:5000/predict", {
      method: "POST",
      body: resizedImage
    });
  };

  onMount(() => {
    if (browser) {
      const canvas = document.getElementById("board") as HTMLCanvasElement,
        context = canvas.getContext("2d");
      var isDrawing = false;

      canvas.height = canvas.offsetHeight;
      canvas.width = canvas.offsetWidth;

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
          isDrawing = true;
          context.beginPath();
        });
        canvas.addEventListener("touchstart", () => {
          isDrawing = true;
          context.beginPath();
        });

        canvas.addEventListener("mouseup", () => {
          isDrawing = false;
          predictImage(canvas);
        });
        canvas.addEventListener("touchend", () => {
          isDrawing = false;
          predictImage(canvas);
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
        <h1>Draw away!</h1>
      </div>
      <canvas id="board" />
    </div>
    <div id="panel">
      <div id="panel__server">
        <h2>Server</h2>
        <p>The game hasn't started yet. Give me a moment!</p>
      </div>
      <div id="panel__model">
        <h2>Model</h2>
        <p>Hurry up already...</p>
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
</style>
