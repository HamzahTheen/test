async function loadDestinations() {
    const response = await fetch('/api/destinations');
    const destinations = await response.json();
  
    const container = document.getElementById('destinations-container');
    container.innerHTML = '';
  
    destinations.forEach(destination => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <img src="${destination.image}" alt="${destination.name}">
        <h3>${destination.name}</h3>
        <p>${destination.description}</p>
      `;
      container.appendChild(card);
    });
  }
  
  document.addEventListener('DOMContentLoaded', loadDestinations);
  