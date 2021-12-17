const table = document.createElement('table');

const tHead = document.createElement('thead');

const trHead = document.createElement('tr');

let th = document.createElement('th');

const tbody = document.createElement('tbody');

const trBody = document.createElement('tr');

let td = document.createElement('td');

tHead.append(trHead)

tbody.append(trBody)

table.append(tHead, tbody)

const headers = ['Name', 'Clinic', 'Address', 'Phone', 'Rating']
headers.forEach(element => {
    let th = document.createElement('th');
    th.innerText = element;
    trHead.appendChild(th)
})


document.body.appendChild(table)

