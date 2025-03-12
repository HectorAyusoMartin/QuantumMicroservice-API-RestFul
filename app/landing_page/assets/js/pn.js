<script>
  // Ajustá e
  stos valores para modificar la velocidad
  const pixelsPorPaso = 1;    // cantidad de píxeles que se desplaza en cada paso
  const intervaloMs = 50;       // intervalo en milisegundos entre cada paso

  function desplazarDerecha() {
    window.scrollBy(pixelsPorPaso, 0);
  }

  // Iniciamos el desplazamiento de forma automática una vez cargada la página
  window.addEventListener('load', function() {
    setInterval(desplazarDerecha, intervaloMs);
  });
</script>
