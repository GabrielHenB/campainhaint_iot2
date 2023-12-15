export const API_BASE = "http://localhost:5000/"


// ENDPOINTS GET
const eventos = "eventos";
const pessoas = "pessoas";
const capturas = "capturas";
const tem_acesso = "api/temacesso"; // Enviar id da Pessoa na querystring
const urli = "api/i/"; // Enviar nome da Imagem na querystring

// ENDPOINTS POST
const salvar = "salvar"; // Enviar id_evento e nome
const upload = "upload"; // Enviar Imagem no request FormData

// ENDPOINTS UPDATE
const pessoas_up = "pessoas/up"; // Enviar id

export const URL_EVENTOS = API_BASE + eventos;
export const URL_PESSOAS = API_BASE + pessoas;
export const URL_PESSOAS_UP = API_BASE + pessoas_up;
export const URL_CAPTURAS = API_BASE + capturas;
export const URL_ACESSO = API_BASE + tem_acesso;
export const URL_I = API_BASE + urli;
export const URL_SALVAR = API_BASE + salvar;
export const URL_UPLOAD = API_BASE + upload;
