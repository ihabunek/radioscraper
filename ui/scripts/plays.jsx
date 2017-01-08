/* global window document playsPath */

import $ from 'jquery'
import URI from 'urijs'

const searchWith = (params) => {
    const uri = new URI()
    uri.removeQuery(["page"])
    uri.setQuery(params)
    window.location.href = uri.toString()
}

const clearSearch = (fields) => {
    fields =  fields || ["artist", "title"]
    const uri = new URI()
    uri.removeQuery(["page"])
    uri.removeQuery(fields)
    window.location.href = uri.toString()
}

const goToPath = (path) => {
    const uri = new URI()
    uri.removeQuery(["page"])
    uri.pathname(path)
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
        goToPath(playsPath + e.target.dataset.radio)
    })

    $('[data-clear-field]').click(e => {
        e.preventDefault()
        clearSearch(e.target.dataset.clearField)
    })

    $('[data-clear-all]').click(e => {
        e.preventDefault()
        window.location.href = playsPath
    })

    $('a[data-paging]').click(e => {
        e.preventDefault()
        searchWith({ "page": e.target.dataset.page })
    })

    $('[data-radio-select]').change(e => {
        e.preventDefault()
        goToPath(playsPath + e.target.value)
    })

    $('[data-clear-radio]').click(e => {
        e.preventDefault()
        goToPath(playsPath)
    })
})
