import $ from 'jquery'
import 'jquery-ui/ui/widgets/datepicker'
import URI from 'urijs'

const searchWith = (params) => {
    const uri = new URI()
    uri.removeQuery(["page"])
    uri.setQuery(params)
    window.location.href = uri.toString()
}

$(document).ready(() => {
    $('a[data-paging]').click(e => {
        e.preventDefault()
        searchWith({ "page": e.target.dataset.page })
    })
})
