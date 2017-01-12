/* global window document */

import $ from 'jquery'
import 'jquery-ui/ui/widgets/datepicker'
import URI from 'urijs'
import moment from 'moment'

const current = () => {
    const year = $('[data-year]').text()
    const month = $('[data-month]').text()

    return moment({
        "year": year,
        "month": month - 1
    })
}

const goToDate = date => {
    const uri = new URI()

    uri.setQuery({
        "year": date.year(),
        "month": date.month() + 1
    })

    window.location = uri.toString()
}

$(document).ready(() => {
    $("[data-next-month]").click(() =>
        goToDate(current().add(1, 'month')))

    $("[data-prev-month]").click(() =>
        goToDate(current().add(-1, 'month')))

    $("[data-next-year]").click(() =>
        goToDate(current().add(1, 'year')))

    $("[data-prev-year]").click(() =>
        goToDate(current().add(-1, 'year')))
})
