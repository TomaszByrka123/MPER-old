import { zapisz_do_tablicy, odczytaj_z_tablicy } from "./function.js"; //no zaladuj sie

const header = document.getElementById('content');

odczytaj_z_tablicy(1)
    .then(data => {
        header.innerHTML = data.message;
    });