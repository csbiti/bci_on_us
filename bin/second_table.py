def second_table(code_banque, date_traitement, montant_BCI, montant_hors_BCI, montant_etrangers):
    return """
        <style type="text/css">  

        .second_table{
            margin-top: 50px;
            border-collapse: collapse;
            border-spacing: 0;
            float: left;
            width: 100%;
        }

        /* ROWS */

        .second_table tr.even {
            background-color: #c6c5c5;
        }

        /* HEADERS */
        .second_table th {
            padding: 20px 10px;
            border-width: 0;
            font-family: Times;
            font-size: 14px;
            font-weight: bold;
            overflow: hidden;
            text-align: left;
        }

        .second_table th.right {
            text-align: right;
        }

        /* CELLS */

        .second_table td {
        border-width: 0;
        font-family: Times;
        font-size: 14px;
        overflow: hidden;
        padding: 20px 10px;
        }

        .second_table td.right {
            text-align: right;
        }

        .second_table td.center {
            text-align: center;
        }

        .second_table td.left {
            text-align: left;
        }
    </style>

    <div> 
        <table class="second_table">
            <tbody>
                <tr>
                    <th>Code Banque</th>
                    <th>Date Traitement</th>
                    <th>Type Retrait </th>
                    <th class="right">Montant Total</th>
                </tr>
                <tr class="even">
                    <td class="center">""" + code_banque + """</td>
                    <td class="center">""" + date_traitement + """</td>
                    <td class="left">retrait porteur bci</td>
                    <td class="right">""" + montant_BCI + """</td>
                </tr>
                <tr>
                    <td class="center"></td>
                    <td class="center"></td>
                    <td class="left">Retraits porteurs francais hors bci</td>
                    <td class="right">""" + montant_hors_BCI + """</td>
                </tr>
                <tr class="even">
                    <td class="center"></td>
                    <td class="center"></td>
                    <td class="left">Retraits porteurs étrangers</td>
                    <td class="right">""" + montant_etrangers + """</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
