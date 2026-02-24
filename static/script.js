const form = document.getElementById("snippetForm");
const snippetsDiv = document.getElementById("snippets");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const snippet = {
        title: document.getElementById("title").value,
        language: document.getElementById("language").value,
        tags: document.getElementById("tags").value,
        code: document.getElementById("code").value
    };

    await fetch("/snippets", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(snippet)
    });

    form.reset();
    loadSnippets();
});

async function loadSnippets() {
    const res = await fetch("/snippets");
    const data = await res.json();

    snippetsDiv.innerHTML = "";

    data.forEach(snippet => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h3>${snippet[1]} (${snippet[2]})</h3>
            <p>Tags: ${snippet[3]}</p>
            <pre>${snippet[4]}</pre>
            <button onclick="deleteSnippet(${snippet[0]})">Delete</button>
            <hr>
        `;
        snippetsDiv.appendChild(div);
    });
}

async function deleteSnippet(id) {
    await fetch(`/snippets/${id}`, { method: "DELETE" });
    loadSnippets();
}

loadSnippets();