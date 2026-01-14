document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('tierlist-container');
    if (!container) return;

    const isOwner = container.dataset.isOwner === 'true';
    console.log("Is Owner:", isOwner);

    if (!isOwner) {
        return;
    }

    const tierItems = document.querySelectorAll('.tier-item');
    const tierRows = document.querySelectorAll('.tier-row');
    const saveOrderButton = document.getElementById('saveOrder');

    tierItems.forEach(item => {
        item.setAttribute('draggable', 'true');
        item.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', this.dataset.id);
            this.classList.add('dragging');
        });

        item.addEventListener('dragend', function(e) {
            this.classList.remove('dragging');
        });
    });

    tierRows.forEach(row => {
        row.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        row.addEventListener('dragleave', function(e) {
            this.classList.remove('drag-over');
        });

        row.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            const itemId = e.dataTransfer.getData('text/plain');
            const draggedItem = document.querySelector(`.tier-item[data-id="${itemId}"]`);
            if (draggedItem) {
                this.appendChild(draggedItem);
                const tier = this.dataset.tier;
                updateTier(itemId, tier);
            }
        });
    });

    function updateTier(itemId, tier) {
        console.log("Updating tier for item:", itemId, "to tier:", tier); // Debugging line

        fetch(`/tierlists/update-tier/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CRFToken': '{{ csrf_token }}',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ tier: tier })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    if (saveOrderButton) {
        saveOrderButton.addEventListener('click', function() {
            const tiers = document.querySelectorAll('.tier-row');
            const orderData = {};

            tiers.forEach(tierRow => {
                const tier = tierRow.dataset.tier;
                const items = tierRow.querySelectorAll('.tier-item');
                orderData[tier] = Array.from(items).map(item => item.dataset.id);
            });

            fetch(`/tierlists/save-order/${container.dataset.tierlistId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(orderData)
            })
            .then(response => response.json())
            .then(data => {
                alert('Order saved successfully!');
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
