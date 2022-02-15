$(document).ready(function () {
    // Récupérer l'ID de la campagne dans la DIV actuelle et l'ajouter en tant que param url
    let campaignsList = $('#campaignsList').children();

    for (let i = 0; i < campaignsList.length; i++) {
        let campaign_id = $('#campaign_id_' + i).text();
        let duplicate_button = $('#campaign_dup_' + i);
        let go_button = $('#campaign_go_' + i);
        let index = i + 1;
        go_button.wrap('<a href="/campagne?c=' + index + '"></a>');
        duplicate_button.wrap('<a href="/campagnes?c=' + index + '"></a>');
    }

});