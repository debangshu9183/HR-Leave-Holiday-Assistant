from src.sql_helper import run_sql
import pandas as pd

def chat_with_hr(user_question, history, client, model, system_prompt, connection):


    history.append({"role": "user", "content": user_question})

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}] + history,
        temperature=0.2,
    )

    reply = response.choices[0].message.content

    if "SQL_QUERY:" in reply:

        sql_line = [line for line in reply.splitlines() if "SQL_QUERY:" in line][0]
        sql_query = sql_line.replace("SQL_QUERY:", "").strip()

        print(f"\n🔍 Running SQL: {sql_query}")

        # Execute SQL
        sql_results = run_sql(sql_query, connection)

        # Convert to dataframe for structured summary
        df = pd.DataFrame(sql_results)

        print("\n📊 SQL Result Table:")
        print(df)

        # Create structured summary prompt
        summary_prompt = f"""


    The user asked: {user_question}

    SQL Query Executed:
    {sql_query}

    SQL Results:
    {df.to_string(index=False)}

    Explain the results clearly.
    Only use the values shown in the SQL results.
    Do not guess or infer missing information.
    """
        history.append({"role": "assistant", "content": reply})
        history.append({"role": "user", "content": summary_prompt})

        response2 = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt}] + history,
            temperature=0.2,
        )

        final_reply = response2.choices[0].message.content
        history.append({"role": "assistant", "content": final_reply})

        return final_reply

    else:
        history.append({"role": "assistant", "content": reply})
        return reply

