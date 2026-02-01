fetch('./data/wods.json')
  .then(response => response.json())
  .then(data => {
    const source = data.sources[0]; // MYLEO כרגע
    const container = document.getElementById('wods');

    let html = '';

    source.wods.forEach(wod => {
      html += `<section>`;
      html += `<h2>${wod.date}</h2>`;

      wod.sections.forEach(section => {
        html += `<h3>${section.title}</h3><ul>`;
        section.lines.forEach(line => {
          html += `<li>${line}</li>`;
        });
        html += `</ul>`;
      });

      html += `</section>`;
    });

    container.innerHTML = html;
  })
  .catch(err => {
    document.getElementById('wods').innerHTML =
      '<p>שגיאה בטעינת האימונים</p>';
  });
