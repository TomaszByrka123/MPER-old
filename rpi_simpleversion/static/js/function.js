export function zapisz_do_tablicy(indeks, wartosc) {
    fetch('/zapisz_do_tablicy', {
        method: 'POST',
        body: JSON.stringify({ indeks: indeks, wartosc: wartosc }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        return data.message;
    });
}

export function odczytaj_z_tablicy(indeks) {
    fetch('/odczytaj_z_tablicy', {
        method: 'POST',
        body: JSON.stringify({indeks: indeks}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        return data.message;
    });
}