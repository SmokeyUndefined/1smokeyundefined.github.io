async function search() {
    var query = document.getElementById("query").value;
    if (!query) {
        alert("Please enter a query");
        return;
    }

    try {
        const results = await fetchResults(query);
        displayResults(results);
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while fetching search results");
    }
}

async function fetchResults(query) {
    const url = `/search?query=${encodeURIComponent(query)}`;
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error('Failed to fetch search results');
    }
    return response.json();
}

function displayResults(results) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    Object.entries(results).forEach(([source, links]) => {
        const header = document.createElement("h2");
        header.textContent = `${source} Results`;
        resultsDiv.appendChild(header);

        links.forEach(link => {
            const anchor = document.createElement("a");
            anchor.href = link;
            anchor.textContent = link;
            resultsDiv.appendChild(anchor);
            resultsDiv.appendChild(document.createElement("br"));
        });
    });
}
