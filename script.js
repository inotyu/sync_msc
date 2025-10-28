let player;
let videoId = '';
let playlist = [];
let indiceVideoAtual = -1;
let paginaAtual = 0;
const videosPorPagina = 2;

function aoCarregarAPIYouTubeIframe() {}

function aoPlayerPronto(event) {
    setInterval(function() {
        if (player && player.getCurrentTime) {
            var tempoAtual = player.getCurrentTime();
            document.getElementById('tempo-atual').textContent = formatarTempo(Math.floor(tempoAtual));
        }
    }, 1000);

    document.getElementById('tocar').addEventListener('click', () => player.playVideo());
    document.getElementById('pausar').addEventListener('click', () => player.pauseVideo());
    document.getElementById('parar').addEventListener('click', () => player.stopVideo());
}

function aoAlterarEstadoPlayer(event) {
    if (event.data === YT.PlayerState.ENDED) {
        carregarProximoVideo();
    }
}

function extrairIdVideo(url) {
    const match = url.match(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/|.+\?v=)|youtu\.be\/)([^"&?\/\s]{11})/);
    return match ? match[1] : null;
}

function formatarTempo(segundos) {
    const minutos = Math.floor(segundos / 60);
    const seg = Math.floor(segundos % 60);
    return `${minutos}:${seg < 10 ? '0' : ''}${seg}`;
}

function configurarPlayer(idVideo) {
    const urlMiniatura = `https://img.youtube.com/vi/${idVideo}/hqdefault.jpg`;
    const imagemMiniatura = document.createElement('img');
    imagemMiniatura.src = urlMiniatura;
    imagemMiniatura.className = 'thumbnail-image';
    const containerMiniatura = document.querySelector('.container-miniatura');
    containerMiniatura.innerHTML = '';
    containerMiniatura.appendChild(imagemMiniatura);
        
    if (player) {
        player.loadVideoById(idVideo);
    } else {
        player = new YT.Player('reprodutor', {
            height: '0',
            width: '0',
            videoId: idVideo,
            playerVars: { 
                'autoplay': 1, 
                'controls': 0,
                'vq': 'hd720' 
            },
            events: {
                'onReady': aoPlayerPronto,
                'onStateChange': aoAlterarEstadoPlayer
            }
        });
    }
}

function carregarProximoVideo() {
    indiceVideoAtual++;
    if (indiceVideoAtual < playlist.length) {
        configurarPlayer(playlist[indiceVideoAtual]);
    } else {
        alert('A playlist terminou.');
        indiceVideoAtual--;
    }
}

function carregarVideoAnterior() {
    indiceVideoAtual--;
    if (indiceVideoAtual >= 0) {
        configurarPlayer(playlist[indiceVideoAtual]);
    } else {
        alert('Você está no primeiro vídeo da playlist.');
        indiceVideoAtual++;
    }
}

function atualizarPlaylist() {
    const containerPlaylist = document.getElementById('miniaturas-playlist');
    containerPlaylist.innerHTML = '';

    const inicio = paginaAtual * videosPorPagina;
    const fim = inicio + videosPorPagina;
    
    playlist.slice(inicio, fim).forEach((idVideo, index) => {
        const urlMiniatura = `https://img.youtube.com/vi/${idVideo}/hqdefault.jpg`;
        const imagemMiniatura = document.createElement('img');
        imagemMiniatura.src = urlMiniatura;
        imagemMiniatura.className = 'miniatura-playlist';
        imagemMiniatura.onclick = () => {
            indiceVideoAtual = inicio + index;
            configurarPlayer(idVideo);
        };
        containerPlaylist.appendChild(imagemMiniatura);
    });

    if (indiceVideoAtual === -1 && playlist.length > 0) {
        indiceVideoAtual = 0;
        configurarPlayer(playlist[indiceVideoAtual]);
    }
}

document.getElementById('carregar-video').addEventListener('click', () => {
    const url = document.getElementById('url-video').value.toLowerCase();
    const palavras = ["mateus", "deborah", "henrique", "gean"];
    const videoId = extrairIdVideo(url);
    const pegar = url; 

    if (palavras.some(palavra => pegar.includes(palavra))) {
        alert('Easter egg descoberto!');
        window.location.href = "https://hiddendeploygean.netlify.app";
        return; 
    }

    if (videoId && !playlist.includes(videoId)) {
        playlist.push(videoId);
        document.getElementById('url-video').value = ''; 
        atualizarPlaylist(); 
        alert('Vídeo adicionado à playlist.');
    } else {
        alert('Link inexistente ou seu vídeo já está na playlist.');
    }
});


document.getElementById('video-anterior').addEventListener('click', carregarVideoAnterior);
document.getElementById('proximo-video').addEventListener('click', carregarProximoVideo);

document.getElementById('proxima-pagina').addEventListener('click', () => {
    if ((paginaAtual + 1) * videosPorPagina < playlist.length) {
        paginaAtual++;
        atualizarPlaylist();
    }
});

document.getElementById('pagina-anterior').addEventListener('click', () => {
    if (paginaAtual > 0) {
        paginaAtual--;
        atualizarPlaylist();
    }
});

atualizarPlaylist();
