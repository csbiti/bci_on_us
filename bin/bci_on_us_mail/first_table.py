def first_table(processus, activite, date, heure):
    return """<style type="text/css">
        .first_table {
            border-collapse: collapse;
            border-spacing: 0;
            width: 70%;
            float: right;
            padding: 0px 0px 0xp 0xp;
            table-layout: fixed;
            width: 80%
        }

        .first_table td {
            border-style: solid;
            border-width: 2px;
            font-family: Arial, sans-serif;
            font-size: 12px;
            overflow: hidden;
            padding: 20px 5px;
            word-break: normal;

        }

        .first_table .title {
            text-align: center;
            vertical-align: middle;
            font-weight: bold;
            font-size: 16px;
            line-height: 1.5
        }

        .first_table .center {
            text-align: center;

        }

        .first_table .left {
            text-align: left;

        }

        .first_table .right {
            text-align: right;
        }

    </style>

    <div>
        <table class="first_table">
            <colgroup>
                <col style="width: 50%">
                <col style="width: 25%">
                <col style="width: 10%">
                <col style="width: 15%">
            </colgroup>
            <tbody>
                <tr>
                    <td class="center">Backoffice Bancaire</td>
                    <td class="left">Processus : """ + processus + """</td>
                    <td class="right">Date :</span>
                    </td>
                    <td class="center">""" + date + """</span>
                    </td>
                </tr>
                <tr>
                    <td class="title" rowspan="2">BCI<br>ECLATEMENT RETRAITS GAB EMV <br>""" + date + """</td>
                    <td class="left">Activité : """ + activite + """</td>
                    <td class="right">Heure : </td>
                    <td class="center">""" + heure + """</td>
                </tr>
                <tr>
                    <td class="left" colspan="3"></td>
                </tr>
            </tbody>
        </table>
    </div>"""
