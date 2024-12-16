/**
 * Populate form fields from GET/POST data in the document
 */
(function () {
    /**
     * Function to get query parameters from the URL
     * @returns {Object} Key-value pairs of query parameters
     */
    function getQueryParams() {
        const params = new URLSearchParams(window.location.search);
        const data = {};
        for (const [key, value] of params) {
            data[key] = value;
        }
        return data;
    }

    /**
     * Populate form fields matching keys from the data object
     * @param {Object} data - Key-value pairs to populate the form fields
     */
    function populateFormFields(data) {
        Object.keys(data).forEach(key => {
            const fields = document.querySelectorAll(`[name="${key}"]`);
            
            fields.forEach(field => {
                if (field.type === "checkbox" || field.type === "radio") {
                    // Set 'checked' if the value matches
                    field.checked = field.value === data[key];
                } else {
                    // Default case: assign the value
                    field.value = data[key];
                }
            });
        });
    }

    // Check for the existence of the prepareForm function and execute it if available
    if (typeof prepareForm === "function") {
        prepareForm();
    }

    // Get GET data from the URL
    const formData = getQueryParams();

    // Populate the form fields
    populateFormFields(formData);
})();
