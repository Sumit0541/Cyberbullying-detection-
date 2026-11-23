const message = document.getElementById("message");
const count = document.getElementById("count");
const scanBtn = document.getElementById("scanBtn");
const errorBox = document.getElementById("error");

message.addEventListener("input", () => {
  count.textContent = `${message.value.length} / 5000`;
});

function addChips(element, items) {
  element.innerHTML = "";
  if (!items || items.length === 0) {
    element.textContent = "None detected";
    return;
  }
  items.forEach(item => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = item;
    element.appendChild(chip);
  });
}

scanBtn.addEventListener("click", async () => {
  errorBox.textContent = "";
  const text = message.value.trim();
  if (!text) {
    errorBox.textContent = "Please enter a message first.";
    return;
  }

  scanBtn.disabled = true;
  scanBtn.textContent = "Analysing...";
  try {
    const response = await fetch("/api/analyse", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed.");

    document.getElementById("emptyState").classList.add("hidden");
    document.getElementById("results").classList.remove("hidden");
    document.getElementById("status").textContent = data.status;
    document.getElementById("risk").textContent = `${data.risk.toUpperCase()} RISK`;
    document.getElementById("risk").className = `risk ${data.risk.toLowerCase()}`;
    document.getElementById("confidence").textContent = `${data.confidence}%`;
    document.getElementById("confidenceBar").style.width = `${data.confidence}%`;
    addChips(document.getElementById("terms"), data.harmful_terms);
    addChips(document.getElementById("categories"), data.categories);
    document.getElementById("explanation").textContent = data.explanation;

    const list = document.getElementById("recommendations");
    list.innerHTML = "";
    data.recommendations.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item;
      list.appendChild(li);
    });
  } catch (error) {
    errorBox.textContent = error.message;
  } finally {
    scanBtn.disabled = false;
    scanBtn.textContent = "✦ Analyse message";
  }
});
