/* global window document */

import $ from 'jquery'
import 'jquery-ui/ui/widgets/datepicker'
import URI from 'urijs'
import moment from 'moment'

const currentDate = () => {
    const year = $('[data-year]').text()
    const month = $('[data-month]').text()

    return moment({
        "year": year,
        "month": month - 1
    })
}

const currentRadio = () => $('[data-radio]').val()

const goTo = (date, radio) => {
    const path = radio ?  `/stats/${radio}/` : '/stats/'
    const uri = URI(path)

    uri.setQuery({
        "year": date.year(),
        "month": date.month() + 1,
    })

    window.location = uri.toString()
}

$(document).ready(() => {
    $("[data-next-month]").click(() => goTo(
        currentDate().add(1, 'month'),
        currentRadio(),
    ))

    $("[data-prev-month]").click(() => goTo(
        currentDate().add(-1, 'month'),
        currentRadio(),
    ))

    $("[data-next-year]").click(() => goTo(
        currentDate().add(1, 'year'),
        currentRadio(),
    ))

    $("[data-prev-year]").click(() => goTo(
        currentDate().add(-1, 'year'),
        currentRadio(),
    ))

    $("[data-radio]").change(() => goTo(
        currentDate(),
        currentRadio(),
    ))
})
