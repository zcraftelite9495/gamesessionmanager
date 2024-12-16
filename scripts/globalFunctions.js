// --------------- Global Functions --------------- 

function redirectToInfo(gameName) {
    // Encode the game name to ensure it's safe for URL parameters
    const encodedName = encodeURIComponent(gameName);
    window.location.href = `/check_game_info?game_name=${encodedName}&autosubmit=1`; // Automatically gets the info using the `autosubmit` parameter
}

function redirectToStopwatch(gameName) {
    // Encode the game name to ensure it's safe for URL parameters
    const encodedName = encodeURIComponent(gameName);
    window.location.href = `/stopwatch?game_name=${encodedName}`;
}

function redirectToManual(gameName) {
    // Encode the game name to ensure it's safe for URL parameters
    const encodedName = encodeURIComponent(gameName);
    window.location.href = `/add_entry?game_name=${encodedName}`;
}

function getGameNameAndRedirectToInfo() {
    // Encode the game name to ensure it's safe for URL parameters
    const gameName = encodeURIComponent(document.getElementById('game_name').value);
    window.location.href = `/check_game_info?game_name=${gameName}&autosubmit=1`; // Automatically gets the info using the `autosubmit` parameter
}

function addOrdinalSuffix(rank) {
    if (rank % 100 >= 11 && rank % 100 <= 13) {
        return rank + "th";
    }
    switch (rank % 10) {
        case 1:
            return rank + "st";
        case 2:
            return rank + "nd";
        case 3:
            return rank + "rd";
        default:
            return rank + "th";
    }
}

// ------------------- Startup -------------------
    
function startup_rankedNumberClassSetup() {
    // Ranked Number Class
    document.querySelectorAll('.ranked-number').forEach(span => {
        const rank = parseInt(span.textContent, 10);
        if (!isNaN(rank)) {
            span.textContent = addOrdinalSuffix(rank);
        }
    });
}

// -------------- Global Injections --------------

document.addEventListener('DOMContentLoaded', function () { // Waits for initial loading to finish
    startup_rankedNumberClassSetup()
});

// --------------- More Functions ----------------

document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('game_name');
    const suggestionsContainer = document.getElementById('suggestions');

    if (input && suggestionsContainer && gamesWithIcons) {
        const games = Object.keys(gamesWithIcons);

        input.addEventListener('input', function () {
            const query = input.value.toLowerCase();
            const matches = games.filter(game => game.toLowerCase().includes(query));

            suggestionsContainer.innerHTML = '';

            if (matches.length > 0) {
                // Display matching suggestions with icons in the dropdown
                matches.forEach(game => {
                    const suggestion = document.createElement('div');
                    suggestion.classList.add('suggestion-item');

                    // Create icon element for dropdown
                    const suggestionIcon = document.createElement('img');
                    suggestionIcon.src = gamesWithIcons[game];
                    suggestionIcon.alt = `${game} icon`;
                    suggestionIcon.style.width = '24px';  // Adjust size as needed
                    suggestionIcon.style.height = '24px'; // Adjust size as needed
                    suggestionIcon.style.marginRight = '8px';

                    // Text node for game name
                    const text = document.createTextNode(game);

                    suggestion.appendChild(suggestionIcon);
                    suggestion.appendChild(text);

                    suggestion.addEventListener('click', () => {
                        input.value = game;
                        if (isCheckInfo) {
                            document.getElementById('game-info-form').requestSubmit();
                        }
                        suggestionsContainer.style.display = 'none';
                    });

                    suggestionsContainer.appendChild(suggestion);
                });
                suggestionsContainer.style.display = 'block';
            } else {
                suggestionsContainer.style.display = 'none';
            }
        });

        input.addEventListener('blur', () => {
            setTimeout(() => suggestionsContainer.style.display = 'none', 100);
        });

        input.addEventListener('focus', () => {
            if (suggestionsContainer.innerHTML !== '') {
                suggestionsContainer.style.display = 'block';
            }
        });
    }
});