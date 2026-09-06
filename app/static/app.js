document.addEventListener('DOMContentLoaded',()=>{
 const master=document.querySelector('#master'); const strength=document.querySelector('#strength');
 if(master){master.addEventListener('input',()=>{const p=master.value;let s=(p.length>=12)+(p.length>=20)+/[A-Z]/.test(p)+/[a-z]/.test(p)+/\d/.test(p)+/[^A-Za-z0-9]/.test(p);strength.textContent=['Very weak','Very weak','Weak','Fair','Strong','Very strong','Excellent'][s]||'Very weak';});}
 const gen=document.querySelector('#gen');
 if(gen){gen.addEventListener('click',async()=>{const r=await fetch('/vault/generate?length=24');const d=await r.json();document.querySelector('#password').value=d.password;document.querySelector('#password').type='text';});}
 const copy=document.querySelector('#copy'); if(copy){copy.addEventListener('click',async()=>{await navigator.clipboard.writeText(document.querySelector('#secret').textContent);copy.textContent='Copied';setTimeout(()=>copy.textContent='Copy password',1500);});}
});
/* =========================================================
   SECUREVAULT - CREDENTIAL FORM
   Password visibility, strength meter and generator
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    const generatePasswordBtn =
        document.getElementById("generatePasswordBtn");

    const sidebarGenerateBtn =
        document.getElementById("sidebarGenerateBtn");

    const strengthProgress =
        document.getElementById("strengthProgress");

    const strengthLabel =
        document.getElementById("strengthLabel");

    const checkLength =
        document.getElementById("checkLength");

    const checkUpper =
        document.getElementById("checkUpper");

    const checkLower =
        document.getElementById("checkLower");

    const checkNumber =
        document.getElementById("checkNumber");

    const checkSymbol =
        document.getElementById("checkSymbol");

    const notes =
        document.getElementById("notes");

    const notesCounter =
        document.getElementById("notesCounter");


    /* =====================================================
       PASSWORD VISIBILITY
       ===================================================== */

    if (togglePassword && passwordInput) {

        togglePassword.addEventListener("click", function () {

            const isPassword =
                passwordInput.type === "password";

            passwordInput.type =
                isPassword ? "text" : "password";

            togglePassword.textContent =
                isPassword ? "🙈" : "👁️";

            togglePassword.setAttribute(
                "aria-label",
                isPassword
                    ? "Hide password"
                    : "Show password"
            );

            togglePassword.setAttribute(
                "title",
                isPassword
                    ? "Hide password"
                    : "Show password"
            );

        });

    }


    /* =====================================================
       PASSWORD STRENGTH
       ===================================================== */

    function evaluatePassword(password) {

        if (!strengthProgress || !strengthLabel) {
            return;
        }

        const checks = {
            length: password.length >= 12,
            upper: /[A-Z]/.test(password),
            lower: /[a-z]/.test(password),
            number: /[0-9]/.test(password),
            symbol: /[^A-Za-z0-9]/.test(password)
        };

        let score = 0;

        Object.values(checks).forEach(function (passed) {
            if (passed) {
                score++;
            }
        });

        if (password.length >= 16) {
            score++;
        }

        let percentage = 0;
        let label = "Not evaluated";

        if (!password) {

            percentage = 0;
            label = "Not evaluated";

        } else if (score <= 2) {

            percentage = 25;
            label = "Weak";

        } else if (score === 3) {

            percentage = 50;
            label = "Fair";

        } else if (score === 4) {

            percentage = 75;
            label = "Strong";

        } else {

            percentage = 100;
            label = "Excellent";

        }

        strengthProgress.style.width =
            percentage + "%";

        strengthLabel.textContent =
            label;


        updateCheck(
            checkLength,
            checks.length
        );

        updateCheck(
            checkUpper,
            checks.upper
        );

        updateCheck(
            checkLower,
            checks.lower
        );

        updateCheck(
            checkNumber,
            checks.number
        );

        updateCheck(
            checkSymbol,
            checks.symbol
        );

    }


    function updateCheck(element, passed) {

        if (!element) {
            return;
        }

        const text =
            element.textContent.replace(
                /^[○✓]\s*/,
                ""
            );

        if (passed) {

            element.textContent =
                "✓ " + text;

            element.classList.add("valid");

        } else {

            element.textContent =
                "○ " + text;

            element.classList.remove("valid");

        }

    }


    if (passwordInput) {

        passwordInput.addEventListener(
            "input",
            function () {
                evaluatePassword(
                    passwordInput.value
                );
            }
        );

        evaluatePassword(
            passwordInput.value
        );

    }


    /* =====================================================
       NOTES COUNTER
       ===================================================== */

    function updateNotesCounter() {

        if (!notes || !notesCounter) {
            return;
        }

        const length =
            notes.value.length;

        notesCounter.textContent =
            length + " / 2000";

    }


    if (notes) {

        notes.addEventListener(
            "input",
            updateNotesCounter
        );

        updateNotesCounter();

    }


    /* =====================================================
       PASSWORD GENERATOR
       ===================================================== */

    async function requestGeneratedPassword() {

        try {

            const response =
                await fetch(
                    "/vault/generate",
                    {
                        method: "GET",
                        credentials: "same-origin",
                        headers: {
                            "Accept": "application/json"
                        }
                    }
                );

            if (!response.ok) {
                throw new Error(
                    "Password generation failed."
                );
            }

            const data =
                await response.json();

            if (
                !data ||
                !data.password
            ) {
                throw new Error(
                    "Invalid generator response."
                );
            }

            return data.password;

        } catch (error) {

            console.error(
                "SecureVault generator:",
                error
            );

            return null;
        }

    }


    /* =====================================================
       GENERATOR MODAL
       ===================================================== */

    let modal = null;
    let generatedPasswordField = null;


    function createGeneratorModal() {

        if (modal) {
            return;
        }

        modal =
            document.createElement("div");

        modal.className =
            "generator-modal";

        modal.innerHTML = `
            <div
                class="generator-modal-card"
                role="dialog"
                aria-modal="true"
                aria-labelledby="generatorTitle"
            >

                <div class="generator-modal-header">

                    <div>
                        <h3 id="generatorTitle">
                            Generate strong password
                        </h3>

                        <p>
                            SecureVault generated this password
                            using the application's password generator.
                        </p>
                    </div>

                    <button
                        type="button"
                        class="generator-close"
                        id="generatorClose"
                        aria-label="Close"
                    >
                        ✕
                    </button>

                </div>

                <div class="generated-password-box">

                    <input
                        type="text"
                        class="generated-password"
                        id="generatedPassword"
                        readonly
                        aria-label="Generated password"
                    >

                    <button
                        type="button"
                        class="copy-generated-btn"
                        id="copyGeneratedPassword"
                    >
                        Copy
                    </button>

                </div>

                <div class="generator-modal-actions">

                    <button
                        type="button"
                        class="regenerate-btn"
                        id="regeneratePassword"
                    >
                        🎲 Regenerate
                    </button>

                    <button
                        type="button"
                        class="use-password-btn"
                        id="useGeneratedPassword"
                    >
                        Use Password
                    </button>

                </div>

            </div>
        `;

        document.body.appendChild(modal);

        generatedPasswordField =
            document.getElementById(
                "generatedPassword"
            );


        /* Close */

        document
            .getElementById("generatorClose")
            .addEventListener(
                "click",
                closeGeneratorModal
            );


        /* Regenerate */

        document
            .getElementById("regeneratePassword")
            .addEventListener(
                "click",
                generateAndDisplayPassword
            );


        /* Use */

        document
            .getElementById("useGeneratedPassword")
            .addEventListener(
                "click",
                useGeneratedPassword
            );


        /* Copy */

        document
            .getElementById("copyGeneratedPassword")
            .addEventListener(
                "click",
                copyGeneratedPassword
            );


        /* Click outside */

        modal.addEventListener(
            "click",
            function (event) {

                if (
                    event.target === modal
                ) {
                    closeGeneratorModal();
                }

            }
        );

    }


    async function openGeneratorModal() {

        createGeneratorModal();

        modal.classList.add("active");

        await generateAndDisplayPassword();

    }


    function closeGeneratorModal() {

        if (!modal) {
            return;
        }

        modal.classList.remove(
            "active"
        );

    }


    async function generateAndDisplayPassword() {

        if (!generatedPasswordField) {
            return;
        }

        generatedPasswordField.value =
            "Generating...";

        const password =
            await requestGeneratedPassword();

        if (!password) {

            generatedPasswordField.value =
                "Generation failed";

            return;
        }

        generatedPasswordField.value =
            password;

    }


    function useGeneratedPassword() {

        if (
            !passwordInput ||
            !generatedPasswordField
        ) {
            return;
        }

        const generated =
            generatedPasswordField.value;

        if (
            !generated ||
            generated === "Generating..." ||
            generated === "Generation failed"
        ) {
            return;
        }

        passwordInput.value =
            generated;

        passwordInput.type =
            "text";

        if (togglePassword) {

            togglePassword.textContent =
                "🙈";

        }

        evaluatePassword(
            generated
        );

        closeGeneratorModal();

        passwordInput.focus();

    }


    async function copyGeneratedPassword() {

        if (!generatedPasswordField) {
            return;
        }

        const password =
            generatedPasswordField.value;

        if (
            !password ||
            password === "Generating..." ||
            password === "Generation failed"
        ) {
            return;
        }

        try {

            await navigator.clipboard.writeText(
                password
            );

            const button =
                document.getElementById(
                    "copyGeneratedPassword"
                );

            if (button) {

                const original =
                    button.textContent;

                button.textContent =
                    "Copied ✓";

                setTimeout(
                    function () {
                        button.textContent =
                            original;
                    },
                    1500
                );

            }

        } catch (error) {

            console.error(
                "Clipboard error:",
                error
            );

        }

    }


    /* =====================================================
       GENERATOR BUTTONS
       ===================================================== */

    if (generatePasswordBtn) {

        generatePasswordBtn.addEventListener(
            "click",
            openGeneratorModal
        );

    }


    if (sidebarGenerateBtn) {

        sidebarGenerateBtn.addEventListener(
            "click",
            openGeneratorModal
        );

    }


    /* =====================================================
       ESCAPE KEY
       ===================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                modal &&
                modal.classList.contains("active")
            ) {

                closeGeneratorModal();

            }

        }
    );

});
/* =========================================================
   SECUREVAULT — CREDENTIAL VIEW
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* -----------------------------------------------------
       Password reveal / hide
       ----------------------------------------------------- */

    const togglePassword = document.getElementById("togglePassword");
    const passwordValue = document.getElementById("passwordValue");
    const maskedPassword = passwordValue
        ? passwordValue.querySelector(".masked-password")
        : null;
    const revealedPassword = passwordValue
        ? passwordValue.querySelector(".revealed-password")
        : null;
    const passwordToggleIcon =
        document.getElementById("passwordToggleIcon");

    let passwordVisible = false;

    if (
        togglePassword &&
        passwordValue &&
        maskedPassword &&
        revealedPassword
    ) {
        togglePassword.addEventListener("click", () => {

            passwordVisible = !passwordVisible;

            if (passwordVisible) {
                maskedPassword.hidden = true;
                revealedPassword.hidden = false;

                togglePassword.setAttribute(
                    "aria-label",
                    "Hide password"
                );

                togglePassword.setAttribute(
                    "title",
                    "Hide password"
                );

                if (passwordToggleIcon) {
                    passwordToggleIcon.textContent = "◌";
                }
            } else {
                maskedPassword.hidden = false;
                revealedPassword.hidden = true;

                togglePassword.setAttribute(
                    "aria-label",
                    "Reveal password"
                );

                togglePassword.setAttribute(
                    "title",
                    "Reveal password"
                );

                if (passwordToggleIcon) {
                    passwordToggleIcon.textContent = "◉";
                }
            }
        });
    }


    /* -----------------------------------------------------
       Copy helpers
       ----------------------------------------------------- */

    const copyToast = document.getElementById("copyToast");
    const copyToastText = document.getElementById("copyToastText");

    let toastTimer = null;

    function showCopyToast(message) {

        if (!copyToast) {
            return;
        }

        if (copyToastText) {
            copyToastText.textContent = message;
        }

        copyToast.hidden = false;

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            copyToast.hidden = true;
        }, 2200);
    }


    async function copyText(value, message = "Copied securely") {

        if (!value) {
            showCopyToast("Nothing to copy");
            return;
        }

        try {

            await navigator.clipboard.writeText(value);

            showCopyToast(message);

        } catch (error) {

            /*
             * Clipboard fallback for browsers where
             * navigator.clipboard is unavailable.
             */

            const textarea = document.createElement("textarea");

            textarea.value = value;
            textarea.style.position = "fixed";
            textarea.style.opacity = "0";
            textarea.style.pointerEvents = "none";

            document.body.appendChild(textarea);

            textarea.focus();
            textarea.select();

            try {
                document.execCommand("copy");
                showCopyToast(message);
            } catch (fallbackError) {
                showCopyToast("Copy failed");
            }

            textarea.remove();
        }
    }


    /* -----------------------------------------------------
       Copy field buttons
       ----------------------------------------------------- */

    const copyButtons =
        document.querySelectorAll("[data-copy-target]");

    copyButtons.forEach((button) => {

        button.addEventListener("click", () => {

            const targetId =
                button.getAttribute("data-copy-target");

            const target =
                document.getElementById(targetId);

            if (!target) {
                return;
            }

            let value = "";

            /*
             * Hidden textarea for notes.
             */
            if (target.tagName === "TEXTAREA") {
                value = target.value;
            }

            /*
             * Credential values.
             */
            else if (target.dataset.value !== undefined) {
                value = target.dataset.value;
            }

            /*
             * Fallback.
             */
            else {
                value = target.textContent.trim();
            }

            let message = "Copied securely";

            if (targetId === "usernameValue") {
                message = "Username copied";
            }

            if (targetId === "passwordValue") {
                message = "Password copied";
            }

            if (targetId === "urlValue") {
                message = "URL copied";
            }

            if (targetId === "notesValue") {
                message = "Notes copied";
            }

            copyText(value, message);
        });

    });


    /* -----------------------------------------------------
       Delete confirmation modal
       ----------------------------------------------------- */

    const deleteButton =
        document.getElementById("deleteEntryButton");

    const deleteModal =
        document.getElementById("deleteModal");

    const closeDeleteModal =
        document.getElementById("closeDeleteModal");

    const cancelDelete =
        document.getElementById("cancelDelete");

    function openDeleteModal() {

        if (!deleteModal) {
            return;
        }

        deleteModal.hidden = false;

        document.body.style.overflow = "hidden";

        if (cancelDelete) {
            setTimeout(() => {
                cancelDelete.focus();
            }, 50);
        }
    }


    function closeModal() {

        if (!deleteModal) {
            return;
        }

        deleteModal.hidden = true;

        document.body.style.overflow = "";
    }


    if (deleteButton) {
        deleteButton.addEventListener("click", openDeleteModal);
    }


    if (closeDeleteModal) {
        closeDeleteModal.addEventListener("click", closeModal);
    }


    if (cancelDelete) {
        cancelDelete.addEventListener("click", closeModal);
    }


    /*
     * Close when clicking outside modal.
     */

    if (deleteModal) {

        deleteModal.addEventListener("click", (event) => {

            if (event.target === deleteModal) {
                closeModal();
            }

        });

    }


    /*
     * Escape key:
     * - close delete modal
     * - hide revealed password
     */

    document.addEventListener("keydown", (event) => {

        if (event.key !== "Escape") {
            return;
        }

        if (deleteModal && !deleteModal.hidden) {
            closeModal();
            return;
        }

        if (passwordVisible && togglePassword) {
            togglePassword.click();
        }

    });


    /* -----------------------------------------------------
       Clear clipboard after a short period
       ----------------------------------------------------- */

    let clipboardClearTimer = null;

    document.addEventListener("click", async (event) => {

        const button =
            event.target.closest("[data-copy-target]");

        if (!button) {
            return;
        }

        const targetId =
            button.getAttribute("data-copy-target");

        if (targetId !== "passwordValue") {
            return;
        }

        /*
         * Clear clipboard after 30 seconds where supported.
         * This reduces accidental exposure from copied passwords.
         */

        clearTimeout(clipboardClearTimer);

        clipboardClearTimer = setTimeout(async () => {

            try {

                const currentClipboard =
                    await navigator.clipboard.readText();

                /*
                 * Only clear if the clipboard still contains
                 * the password that SecureVault copied.
                 */

                const passwordElement =
                    document.getElementById("passwordValue");

                const password =
                    passwordElement?.dataset.value;

                if (
                    password &&
                    currentClipboard === password
                ) {
                    await navigator.clipboard.writeText("");
                }

            } catch (error) {
                /*
                 * Clipboard read/write permissions may be
                 * unavailable. Fail silently.
                 */
            }

        }, 30000);

    });

});
