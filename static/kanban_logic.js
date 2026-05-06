
// static/js/kanban_logic.js
function kanbanBoard() {
    return {
        draggedCard: null,
        
        handleDragStart(event, cardId) {
            this.draggedCard = event.target;
            event.dataTransfer.effectAllowed = 'move';
            // Sürüklenen kartın ID'sini taşıyalım
            event.dataTransfer.setData('text/plain', cardId);
            event.target.style.opacity = '0.5';
        },

        handleDragEnd(event) {
            event.target.style.opacity = '1';
        },

        handleDrop(event, columnStatus) {
            event.preventDefault();
            const cardId = event.dataTransfer.getData('text/plain');
            // Burada kartı yeni sütuna görsel olarak taşıma ve 
            // TAL-39'da HTMX ile veri gönderme işlemleri yapılacak.
            console.log(`Kart ${cardId}, ${columnStatus} sütununa taşındı.`);
        }
    }
}