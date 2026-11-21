document.querySelectorAll("[data-elo-voltar]").forEach((link) => {
    link.addEventListener("click", (event) => {
        if (event.defaultPrevented || event.button !== 0 ||
            event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) {
            return;
        }

        // A visita direta continua usando o destino do link.
        const navigation = window.navigation;
        const previousEntry = navigation?.entries()[navigation.currentEntry.index - 1];
        const previousUrl = previousEntry?.url || document.referrer;
        if (history.length < 2 || !previousUrl ||
            new URL(previousUrl).origin !== location.origin) {
            return;
        }

        event.preventDefault();
        history.back();
    });
});
