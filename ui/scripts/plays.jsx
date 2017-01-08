/* global window document */

import $ from 'jquery'
import 'jquery-ui/ui/widgets/datepicker'
import URI from 'urijs'

const searchWith = (params) => {
    const uri = new URI()
    uri.removeQuery(["page"])
    uri.setQuery(params)
    window.location.href = uri.toString()
}

const clearSearch = (fields) => {
    fields =  fields ? fields : ["artist", "title", "radio", "start", "end"]

    const uri = new URI()
    uri.removeQuery(["page"])
    uri.removeQuery(fields)
    window.location.href = uri.toString()
}

$(document).ready(() => {
    $('a[data-artist]').click(e => {
        e.preventDefault()
        searchWith({ "artist": e.target.dataset.artist })
    })

    $('a[data-title]').click(e => {
        e.preventDefault()
        searchWith({ "title": e.target.dataset.title })
    })

    $('a[data-radio]').click(e => {
        e.preventDefault()
        searchWith({ "radio": e.target.dataset.radio })
    })

    $('a[data-clear-field]').click(e => {
        e.preventDefault()
        clearSearch(e.target.dataset.clearField.split(','))
    })

    $('[data-clear-all]').click(e => {
        e.preventDefault()
        clearSearch()
    })

    $('a[data-paging]').click(e => {
        e.preventDefault()
        searchWith({ "page": e.target.dataset.page })
    })

    const dateFormat = "dd.mm.yy";

    const options = {
        "firstDay": 1,
        "dateFormat": dateFormat,
    }

    const startDatepicker = $('.time-span > input[name=start]').datepicker(options)

    const endDatepicker = $('.time-span > input[name=end]').datepicker(options)

    const getDate = element => {
        try {
            return $.datepicker.parseDate(dateFormat, element.value)
        } catch( error ) {
            return null
        }
    }

    startDatepicker.on("change", e => {
        console.log(getDate(e.target))
        endDatepicker.datepicker("option", "minDate", getDate(e.target))
    })

    endDatepicker.on("change", e => {
        console.log(getDate(e.target))
        startDatepicker.datepicker("option", "maxDate", getDate(e.target))
    })
})
