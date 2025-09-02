# Bot de Clima para Discord 🌤️🌧️

Este é um bot de Discord feito em Python que fornece informações sobre o clima e a chance de chuva em cidades do Brasil e do mundo.  

---

## Funcionalidades

- **Comando `!clima <cidade>`**  
  Mostra a temperatura, sensação térmica, umidade e condição do tempo de uma cidade.

- **Comando `!chuva <cidade>`**  
  Mostra a previsão de chuva para as próximas ~18 horas, com porcentagem de chance e uma frase aleatória divertida.

- **Comando `!olá`**  
  Saudação do bot.

- **Tratamento de erros**  
  - Mensagem amigável se o comando não existir  
  - Aviso caso a cidade não seja encontrada  

---

## Tecnologias e Bibliotecas

- Python 3.10+  
- [discord.py](https://discordpy.readthedocs.io/en/stable/)  
- [requests](https://pypi.org/project/requests/)  
- API do [OpenWeatherMap](https://openweathermap.org/api)  

---

## Como usar

1. Clone este repositório:
```bash
git clone https://github.com/miguelfreitas0901/Bot-discord-Clima.git