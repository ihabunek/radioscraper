/* Common JS functionality, loaded for every page */

require('../styles/app.scss')
require('jquery-ui/themes/base/datepicker.css')

import $ from 'jquery'


$(document).ready(() => {

    // Radio links
    $("[data-radio-link]").click(e => {
        const slug = e.target.dataset.radioLink
        window.location.href = playsPath + "?radio=" + slug
        e.preventDefault()
    })

})

/* global window document playsPath */
