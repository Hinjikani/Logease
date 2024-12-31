const tableDiv = document.getElementById("table");

const updateUrl = (prev, query) => {
  return (
    prev +
    (prev.indexOf("?") >= 0 ? "&" : "?") +
    new URLSearchParams(query).toString()
  );
};

const editableCellAttributes = (data, row, col) => {
  if (row) {
    return { contentEditable: "true", "data-element-id": row.cells[0].data };
  } else {
    return {};
  }
};

new gridjs.Grid({
  columns: [
    { id: "id", name: "Armada ID" },
    { id: "armada_name", name: "Name", sort: false, attributes: editableCellAttributes },
    { id: "armada_email", name: "Armada Email" },
    { id: "armada_phone", name: "Phone Number", sort: false, attributes: editableCellAttributes },
    { id: "capacity", name: "capacity" },
    { id: "armada_status", name: "Status"},
  ],
  server: {
    url: "/api/data/armada",
    then: (results) => results.data,
    total: (results) => results.total,
  },
  search: {
    enabled: true,
    server: {
      url: (prev, search) => {
        return updateUrl(prev, { search });
      },
    },
  },
  sort: {
    enabled: true,
    multiColumn: true,
    server: {
      url: (prev, columns) => {
        const columnIds = ["armada_id", "armada_name", "armada_email", "armada_phone", "capacity", "receiver", "order_fee", "armada_id", "user_id", "status"];
        const sort = columns.map(
          (col) => (col.direction === 1 ? "+" : "-") + columnIds[col.index]
        );
        return updateUrl(prev, { sort });
      },
    },
  },
  pagination: {
    enabled: true,
    server: {
      url: (prev, page, limit) => {
        return updateUrl(prev, { start: page * limit, length: limit });
      },
    },
  },
}).render(tableDiv);

let savedValue;

tableDiv.addEventListener("focusin", (ev) => {
  if (ev.target.tagName === "TD") {
    savedValue = ev.target.textContent;
  }
});

tableDiv.addEventListener("focusout", (ev) => {
  if (ev.target.tagName === "TD") {
    if (savedValue !== ev.target.textContent) {
      fetch("/api/data/armada", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id: ev.target.dataset.elementId,
          [ev.target.dataset.columnId]: ev.target.textContent,
        }),
      });
    }
    savedValue = undefined;
  }
});

tableDiv.addEventListener("keydown", (ev) => {
  if (ev.target.tagName === "TD") {
    if (ev.key === "Escape") {
      ev.target.textContent = savedValue;
      ev.target.blur();
    } else if (ev.key === "Enter") {
      ev.preventDefault();
      ev.target.blur();
    }
  }
});
