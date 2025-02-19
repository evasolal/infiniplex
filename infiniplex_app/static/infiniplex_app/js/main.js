document.addEventListener('DOMContentLoaded', function () {

    const table = document.querySelector('table');
    const headers = table.querySelectorAll('th');

    headers.forEach((header, index) => {
        header.addEventListener('click', () => {
            sortTableByColumn(table, index);
        });
    });


    const searchInput = document.getElementById('search-input');

    if (searchInput) {
        searchInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.form.submit();
            }
        });
    }

    function searchPatientTable(searchText) {
        const query = searchText.toLowerCase().trim();

        if (!query) {
            document.querySelectorAll('table tbody tr').forEach(row => {
                row.style.display = '';
            });
            return;
        }

        const headerCells = document.querySelectorAll('table thead th');
        let patientIdColIdx = -1;
        let outcomeColIdx = -1;

        // Find the column indexes for Patient ID and Outcome
        headerCells.forEach((cell, index) => {
            const headerText = cell.textContent.toLowerCase();
            if (headerText.includes('patient') && headerText.includes('id')) {
                patientIdColIdx = index;
            } else if (headerText.includes('outcome')) {
                outcomeColIdx = index;
            }
        });

        // If we couldn't find the right columns, fall back to a general search
        const useSpecificColumns = (patientIdColIdx !== -1 || outcomeColIdx !== -1);

        // Search through table rows
        const rows = document.querySelectorAll('table tbody tr');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            let matched = false;

            if (useSpecificColumns) {
                // Check patient ID column if found
                if (patientIdColIdx !== -1 && patientIdColIdx < cells.length) {
                    const cellText = cells[patientIdColIdx].textContent.toLowerCase();
                    if (cellText.includes(query)) {
                        matched = true;
                    }
                }

                // Check outcome column if found
                if (!matched && outcomeColIdx !== -1 && outcomeColIdx < cells.length) {
                    const cellText = cells[outcomeColIdx].textContent.toLowerCase();
                    if (cellText.includes(query)) {
                        matched = true;
                    }
                }
            } else {
                cells.forEach(cell => {
                    if (cell.textContent.toLowerCase().includes(query)) {
                        matched = true;
                    }
                });
            }

            row.style.display = matched ? '' : 'none';
        });
    }

    document.getElementById('page-select').addEventListener('change', function() {
        navigateToPage(this.value);
    });

    document.getElementById('id_rows_cnt').addEventListener('change', function() {
        this.form.submit();
    });

    function navigateToPage(pageNumber) {
        window.location.href = '?page=' + pageNumber;
    }
});
