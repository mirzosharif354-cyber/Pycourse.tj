// MyCourse.tj — admin.js
function confirmDel(form) {
    return confirm('Ҳақиқатан ҳазф кунем?');
}
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('form[data-confirm]').forEach(function(f) {
        f.addEventListener('submit', function(e) {
            if (!confirm(f.dataset.confirm)) e.preventDefault();
        });
    });
});
