fetch('./data/wods.json')
  .then(response => response.json())
  .then(data => {
    // שליפה בסיסית – המקור הראשון
    const source = data.sources[0];

    // יצירת HTML פשוט
    let html = `<h1>${source.name}</h1>`;

    source.wods.forEach(wod => {
      html += `<h2>${wod.date}</h2>`;

      wod.sections.forEach(section => {
        html += `<h3>${section.title}</h3><ul>`;
        section.lines.forEach(line => {
          html += `<li>${line}</li>`;
        });
        html += `</ul>`;
      });
    });

    document.body.innerHTML = html;
  })
  .catch(err => {
    document.body.innerHTML = '<h1>שגיאה בטעינת הנתונים</h1>';
  });
