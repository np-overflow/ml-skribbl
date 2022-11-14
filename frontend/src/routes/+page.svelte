<script lang="ts">
  import { browser } from "$app/environment";
  import { onMount } from "svelte";
  import "iconify-icon";

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
        });
        canvas.addEventListener("touchend", () => {
          isDrawing = false;
        });
      }
    }
  });
</script>

<main>
  <section>
    <div>
      <iconify-icon icon="material-symbols:draw-rounded" style="font-size: 2em;" />
      <h1>Draw away!</h1>
    </div>
    <canvas id="board" />
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
    height: 75%;
    width: 75%;
    z-index: 1;
    background-color: white;
    border-radius: 1rem;
    display: flex;
    flex-direction: column;
  }

  section div {
    margin: 2em;
    display: flex;
    align-items: center;
    gap: 1em;
  }

  canvas {
    flex: 1;
    border-top: 2px solid #e5e5e5;
  }
</style>
