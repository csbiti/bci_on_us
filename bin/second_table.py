def second_table(processus, activite, date, heure):
    return """<style type="text/css">
        .tg {
            border-collapse: collapse;
            border-spacing: 0;
            width: 70%;
            float: right;
            padding: 0px 0px 0xp 0xp;
        }

        .tg td {
            border-style: solid;
            border-width: 2px;
            font-family: Arial, sans-serif;
            font-size: 12px;
            overflow: hidden;
            padding: 20px 5px;
            word-break: normal;

        }

        .tg .title {
            text-align: center;
            vertical-align: middle;
            font-weight: bold;
            font-size: 16px;
            line-height: 1.5
        }

        .tg .center {
            text-align: center;

        }

        .tg .left {
            text-align: left;

        }

        .tg .right {
            text-align: right;
        }

    </style>


    <table class="tg" style="undefined;table-layout: fixed; width: 80%">
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
    </table>"""
