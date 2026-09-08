(function () {
    'use strict';

    const LIGHT_TEXT_COLOR = '#111827';
    const DARK_TEXT_COLOR = '#ffffff';

    function currentTextColor() {
        return document.documentElement.classList.contains('dark')
            ? DARK_TEXT_COLOR
            : LIGHT_TEXT_COLOR;
    }

    function applyTheme(editor) {
        if (!editor || editor.status !== 'ready' || !editor.editable()) {
            return;
        }

        const editableElement = editor.editable().$;
        const color = currentTextColor();
        editableElement.style.setProperty('color', color, 'important');
        editableElement.style.setProperty('caret-color', color, 'important');
    }

    function syncEditors() {
        if (!window.CKEDITOR) {
            return;
        }

        Object.values(window.CKEDITOR.instances).forEach(applyTheme);
    }

    function connectCKEditor() {
        if (!window.CKEDITOR) {
            return false;
        }

        window.CKEDITOR.on('instanceReady', function (event) {
            applyTheme(event.editor);
        });
        syncEditors();
        return true;
    }

    document.addEventListener('DOMContentLoaded', function () {
        const observer = new MutationObserver(syncEditors);
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class'],
        });

        if (connectCKEditor()) {
            return;
        }

        let attempts = 0;
        const connectTimer = window.setInterval(function () {
            attempts += 1;
            if (connectCKEditor() || attempts >= 40) {
                window.clearInterval(connectTimer);
            }
        }, 250);
    });
})();
