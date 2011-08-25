<html>
<head>
<b>Account-Chart Enhanced</b> requested by ${user.name}
</head>

  <body>
    <style  type="text/css">
     table {
       border-collapse: collapse;
       cellspacing="0";
       font-size:10px;
           }
     td {margin: 0px; padding: 3px; border: 1px solid lightgrey;  vertical-align: top; }
    </style> 
<p>
Selection:
%if context['data'] :

  <table>
	    <tr>
	    <td>current year: ${context['data']['form']['period_from_name']} - ${context['data']['form']['period_to_name']}</td>
	    <td>previous year: ${context['data']['form']['period_prev_from_name']} - ${context['data']['form']['period_prev_to_name']}</td>
%if context['data']['form']['print_previous_1000'] == 1:
	    <td>previous year in 1000</td>
%endif
%if context['data']['form']['print_views_only'] == 1:
	    <td>print only views</td>
%endif
	    </tr>
  </table>

%else:
  <table>
	    <tr>
	    <td>current: all posted</td>
            <td>previous: year to current month </td> 
	    </tr>
  </table>
%endif
</p>

<%chapter.__init__()%>

<%setLang(user.context_lang)%>
    <table  >

     <thead >
        <tr>
%if context['data']['form']['print_chapter'] == 1:
          <td>Chapter</td>
%endif
          <td>Code</td>
          <td>Name</td>
%if context['data']['form']['print_opening_dc'] == 1:
          <td align="right">Opening Balance</td>
          <td align="right">Debit</td>
          <td align="right">Credit</td>
%endif
          <td align="right">Balance</td>
          <td align="right">Balance Prev</td>
          <td align="right">Balance Diff</td>
          <td align="right">Diff %</td>
        </tr>
      </thead>


 %for account in objects :
     <tbody >
              %if (account.balance_sum !=0 or account.debit_sum !=0 or account.credit_sum !=0 or account.balance_prev_sum !=0 or \
                  context['data']['form']['print_all_zero'] == 1) \
                  and ((account.type == 'view' and context['data']['form']['print_views_only'] == 1) or context['data']['form']['print_views_only'] == 0) :
              <tr>
%if context['data']['form']['print_chapter'] == 1:
          <td>
              %if account.type == 'view':
                 ${chapter.get_structure(account.level) or ''|entity}
              %endif  
          </td>
%endif
          <td>${account.code or ''|entity}  </td>
          <td>
              %if account.type == 'view' :
                <b>
              %endif
               ${account.name or ''|entity}  
              %if account.type == 'view' :
                </b>
              %endif
          </td>
%if context['data']['form']['print_opening_dc'] == 1:
          <td style="text-align:right;white-space:nowrap;">${formatLang(account.opening_balance_sum) }</td>
          <td style="text-align:right;white-space:nowrap;">${formatLang(account.debit_sum)}</td>
          <td style="text-align:right;white-space:nowrap;">${formatLang(account.credit_sum)}</td>
%endif
          <td style="text-align:right;white-space:nowrap;">${formatLang(account.balance_sum)}</td>
%if context['data']['form']['print_previous_1000'] == 1:
          <td style="text-align:right;white-space:nowrap;">${formatLang(round(account.balance_prev_sum/1000,0),digits=0)}</td>
          <td style="text-align:right;white-space:nowrap;">${formatLang(round((account.balance_sum - account.balance_prev_sum)/1000,0),digits=0)} </td>
%else:
          <td style="text-align:right;white-space:nowrap;">${formatLang(account.balance_prev_sum)}</td>
          <td style="text-align:right;white-space:nowrap;">${formatLang(account.balance_sum - account.balance_prev_sum)} </td>

%endif
          <td style="text-align:right;white-space:nowrap;">
                %if account.balance_prev_sum and round(account.balance_prev_sum,2) != 0 and round(account.balance_sum,2) != 0 and (account.balance_sum/abs(account.balance_sum)) == (account.balance_prev_sum /abs(account.balance_prev_sum)):
                 ${formatLang(round(((account.balance_sum - account.balance_prev_sum)/account.balance_prev_sum )*100,2))} 
                %elif round(account.balance_prev_sum,2) != 0 and round(account.balance_sum,2) == 0:
                 ${formatLang(-100)}
                %elif round(account.balance_sum - account.balance_prev_sum,2) == 0 :
                 ${formatLang(0)}
                %else:
                  -
                %endif 
          </td>
        </tr>
            %endif
      </tbody>
 %endfor
    </table>


  </body>
</html>
