document.addEventListener("DOMContentLoaded", () => {
  const resultContainer = document.getElementById("result");
  const text = resultContainer.innerText;

  // Split text into quoted and normal segments
  const segments = text.split(/(".*?")/g);

  const processedSegments = segments.map(segment => {
    if (segment.startsWith('"') && segment.endsWith('"')) {
      const clean = segment.replace(/"/g, "");
      return `<span class="clickable-word" data-word="${clean}">${segment}</span>`;
    }

    return segment.split(/(\s+)/).map(token => {
      const cleanWord = token.replace(/[.,]/g, "");
      if (cleanWord.length > 2) {
        return `<span class="clickable-word" data-word="${cleanWord}">${token}</span>`;
      }
      return token;
    }).join("");
  });

  resultContainer.innerHTML = processedSegments.join("");

  // Click handling to mimic form submit
  resultContainer.addEventListener("click", (e) => {
    if (e.target.classList.contains("clickable-word")) {
      const word = e.target.dataset.word;
      
      // Create and submit a form dynamically
      const form = document.createElement("form");
      form.method = "POST";
      form.action = ""; // same page

      // CSRF token
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const csrfInput = document.createElement("input");
      csrfInput.type = "hidden";
      csrfInput.name = "csrfmiddlewaretoken";
      csrfInput.value = csrfToken;
      form.appendChild(csrfInput);

      // Query input
      const queryInput = document.createElement("input");
      queryInput.type = "hidden";
      queryInput.name = "query";
      queryInput.value = word;
      form.appendChild(queryInput);

      document.body.appendChild(form);
      form.submit();
    }
  });
});
