/* Common JS functionality, loaded for every page */

require('../styles/app.scss')
require('jquery-ui/themes/base/datepicker.css')

import $ from 'jquery'
import 'foundation-sites/dist/js/foundation'

$(document).ready(() => {

    // Radio links
    $("[data-radio-link]").click(e => {
        const slug = e.currentTarget.dataset.radioLink
        window.location.href = playsPath + "?radio=" + slug
        e.preventDefault()
    })

    // Kickstart Foundation JS
    $(document).foundation()
})

/* global window document playsPath */
