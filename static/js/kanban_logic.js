// static/js/kanban_logic.js

function kanbanBoard() {
    return {
        draggedCard: null,

        handleDragStart(event, cardId) {
            this.draggedCard = event.target;
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', cardId);
            event.target.style.opacity = '0.4';
        },

        handleDragEnd(event) {
            event.target.style.opacity = '1';
        },

        handleDrop(event, columnStatus) {
            event.preventDefault();
            const cardId = event.dataTransfer.getData('text/plain');
            
            // Eğer kart geçerli değilse işlem yapma
            if (!cardId) return;

            // Django endpoint URL'si (dashboard namespace'inden)
            const url = `/dashboard/update-status/${cardId}/`;
            
            // Django CSRF token'ı sayfadaki hidden inputtan oku
            const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenElement ? csrfTokenElement.value : '';

            const formData = new FormData();
            formData.append('status', columnStatus);
            if (csrfToken) {
                formData.append('csrfmiddlewaretoken', csrfToken);
            }

            // Sessizce arka planda veritabanı durumunu güncelle
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }).then(response => {
                if (response.ok) {
                    // Kartı görsel olarak yeni sütunun container'ına taşıyalım
                    const card = document.querySelector(`[data-id="${cardId}"]`);
                    const column = event.currentTarget;
                    const container = column.querySelector('.cards-container');
                    
                    if (card && container) {
                        // Eğer sütundaki empty-placeholder ("Kart yok") varsa kaldıralım
                        const emptyPlaceholder = container.querySelector('.empty-placeholder');
                        if (emptyPlaceholder) {
                            emptyPlaceholder.remove();
                        }

                        // Kartı yeni sütuna ekle
                        container.appendChild(card);
                        
                        // Sürüklenen kartın eski sütununu kontrol et ve boş kaldıysa placeholder ekle
                        this.cleanupEmptyColumns();

                        // Sütunların başlarındaki sayaç sayılarını senkronize et
                        this.updateColumnCounters();
                    }
                } else {
                    console.error('Kart durumu veritabanında güncellenemedi.');
                }
            }).catch(error => {
                console.error('Ağ hatası:', error);
            });
        },

        cleanupEmptyColumns() {
            document.querySelectorAll('.cards-container').forEach(container => {
                const cards = container.querySelectorAll('.job-card');
                if (cards.length === 0 && !container.querySelector('.empty-placeholder')) {
                    const placeholder = document.createElement('div');
                    placeholder.className = 'text-center py-5 text-white-50 small empty-placeholder';
                    placeholder.textContent = 'Kart yok';
                    container.appendChild(placeholder);
                }
            });
        },

        updateColumnCounters() {
            document.querySelectorAll('.kanban-column').forEach(column => {
                const cardCount = column.querySelectorAll('.job-card').length;
                const badge = column.querySelector('.badge');
                if (badge) {
                    badge.textContent = cardCount;
                }
            });
        }
    }
}
