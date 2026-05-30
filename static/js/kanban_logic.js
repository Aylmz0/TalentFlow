// static/js/kanban_logic.js

document.addEventListener('DOMContentLoaded', function () {
    // 1. Her bir cards-container için SortableJS'i başlatıyoruz
    document.querySelectorAll('.cards-container').forEach(container => {
        new Sortable(container, {
            group: 'kanban', // Diğer sütunlarla kart paylaşımı için aynı grup ismini veriyoruz
            animation: 250, // Pürüzsüz yer değiştirme animasyonu hızı (ms)
            ghostClass: 'kanban-card-ghost', // Taşınırken arkada kalan gölge sınıfı
            chosenClass: 'kanban-card-chosen', // Sürüklenmek üzere seçilen kart sınıfı
            dragClass: 'kanban-card-drag', // Sürüklenme esnasındaki kart sınıfı
            
            // Kart bir sütundan diğerine taşınıp bırakıldığında tetiklenir
            onEnd: function (evt) {
                const cardId = evt.item.getAttribute('data-id');
                // Bırakılan yeni sütunun durum değerini al
                const newContainer = evt.to;
                const columnStatus = newContainer.getAttribute('data-status');
                
                if (!cardId || !columnStatus) return;
                
                // Arka planda veritabanı durumunu güncellemek için URL
                const url = `/dashboard/update-status/${cardId}/`;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
                
                const formData = new FormData();
                formData.append('status', columnStatus);
                if (csrfToken) {
                    formData.append('csrfmiddlewaretoken', csrfToken);
                }
                
                // Sunucuya sessiz güncelleme isteği at
                fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                }).then(response => {
                    if (response.ok) {
                        // Sayaçları ve boş sütun durumlarını güncelle
                        updateColumnCounters();
                        cleanupEmptyColumns();
                    } else {
                        console.error('Kart durumu veritabanında güncellenemedi.');
                    }
                }).catch(error => {
                    console.error('Ağ hatası:', error);
                });
            }
        });
    });

    // 2. Boş kalan sütunlar için "Kart yok" uyarısı ekleme/silme fonksiyonu
    function cleanupEmptyColumns() {
        document.querySelectorAll('.cards-container').forEach(container => {
            const cards = container.querySelectorAll('.job-card');
            const emptyPlaceholder = container.querySelector('.empty-placeholder');
            
            if (cards.length === 0) {
                if (!emptyPlaceholder) {
                    const placeholder = document.createElement('div');
                    placeholder.className = 'text-center py-5 text-white-50 small empty-placeholder';
                    placeholder.textContent = 'Kart yok';
                    container.appendChild(placeholder);
                }
            } else {
                if (emptyPlaceholder) {
                    emptyPlaceholder.remove();
                }
            }
        });
    }

    // 3. Sütunların başlarındaki sayaç rozetlerini güncelleme fonksiyonu
    function updateColumnCounters() {
        document.querySelectorAll('.kanban-column').forEach(column => {
            const container = column.querySelector('.cards-container');
            if (container) {
                // Sütun içindeki gerçek kartların sayısını al (boş uyarıları sayılmaz)
                const cardCount = container.querySelectorAll('.job-card').length;
                const badge = column.querySelector('.badge');
                if (badge) {
                    badge.textContent = cardCount;
                }
            }
        });
    }

    // Sayfa ilk yüklendiğinde boş sütunları ve sayaçları bir kere kontrol et
    cleanupEmptyColumns();
    updateColumnCounters();
});
