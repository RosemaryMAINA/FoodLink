async function generate() {
  const status = document.getElementById("status");
  const ingredients = document.getElementById("ingredients").value.trim();
  if (!ingredients) {
    status.textContent = "Please enter at least one ingredient.";
    return;
  }
  status.textContent = "Generating recipes…";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Failed to generate");
    renderResults(data.recipes || []);
    status.textContent = "";
  } catch (e) {
    status.textContent = "Error: " + e.message;
  }
}

function renderResults(recipes) {
  const results = document.getElementById("results");
  results.innerHTML = "";
  for (const r of recipes) {
    const div = document.createElement("div");
    div.className = "recipe";
    div.innerHTML = `
      <h3>${r.title}</h3>
      <div><span class="badge">Nutrition: ${r.nutrition_score ?? 70}/100</span></div>
      <p><strong>Ingredients:</strong> ${r.ingredients.join(", ")}</p>
      <p><strong>Steps:</strong></p>
      <ol>${r.steps.map(s => `<li>${s}</li>`).join("")}</ol>
      <div class="actions">
        <button data-action="save">Save</button>
        <button data-action="buy">Buy missing items</button>
      </div>
    `;
    div.querySelector('[data-action="save"]').addEventListener("click", async () => {
      await fetch("/api/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "save_recipe", recipe: r })
      });
      alert("Saved!");
    });
    div.querySelector('[data-action="buy"]').addEventListener("click", async () => {
      const resp = await fetch("/api/payment/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items: r.missing_items || [] })
      });
      const data = await resp.json();
      if (data.checkout_url) {
        window.open(data.checkout_url, "_blank");
      } else {
        alert("Checkout not available.");
      }
    });
    results.appendChild(div);
  }
}

document.getElementById("generateBtn").addEventListener("click", generate);
