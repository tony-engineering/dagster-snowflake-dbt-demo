import os
from pathlib import Path
import dagster as dg
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dagster import asset, OpExecutionContext
from dagster_dbt import DbtCliResource

from dagster_demo.defs.project import dbt_project


@asset(
    group_name="french_tech_insights", 
    compute_kind="Report",
    deps=[
        "stg_french_data_companies",
        "french_tech_companies_summary"
    ]
)
def create_french_tech_report(
    context: OpExecutionContext,
    dbt: DbtCliResource
) -> None:
    """
    Generate a comprehensive interactive report analyzing French tech companies.
    
    The report includes:
    - Company size distribution
    - Industry breakdown
    - Regional analysis
    - Company era trends
    - Geographic distribution
    - Data quality metrics
    
    Args:
        context: The Dagster execution context
        stg_french_data_companies: Dependency on the staging table
        french_tech_companies_summary: Dependency on the summary table
    """
    
    # Get DuckDB path for HTML file storage (following established pattern)
    duckdb_database_path = Path(dbt_project.project_dir).parent / "data" / "dbt_demo.duckdb"
    
    # Connect to Snowflake to get the actual data
    context.log.info("Connecting to Snowflake to load data")
    
    # Get Snowflake connection parameters from environment
    import os
    snowflake_config = {
        'account': os.getenv('SNOWFLAKE_ACCOUNT'),
        'user': os.getenv('SNOWFLAKE_USER'),
        'password': os.getenv('SNOWFLAKE_PASSWORD'),
        'role': os.getenv('SNOWFLAKE_ROLE'),
        'database': os.getenv('SNOWFLAKE_DATABASE'),
        'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
        'schema': os.getenv('SNOWFLAKE_SCHEMA')
    }
    
    try:
        # Connect to Snowflake
        import snowflake.connector
        snowflake_conn = snowflake.connector.connect(**snowflake_config)
        cursor = snowflake_conn.cursor()
        
        context.log.info("Connected to Snowflake successfully")
        
        # Load main companies data from Snowflake
        cursor.execute("""
            SELECT * FROM stg_french_data_companies
            ORDER BY company_name
        """)
        
        # Fetch data and convert to DataFrame
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df_companies = pd.DataFrame(data, columns=columns)
        
        context.log.info(f"Loaded {len(df_companies)} companies from Snowflake staging table")
        
        # Try to load summary data if available
        df_summary = None
        try:
            cursor.execute("""
                SELECT * FROM french_tech_companies_summary
                ORDER BY summary_type, period
            """)
            summary_columns = [desc[0] for desc in cursor.description]
            summary_data = cursor.fetchall()
            df_summary = pd.DataFrame(summary_data, columns=summary_columns)
            context.log.info(f"Loaded summary data with {len(df_summary)} records from Snowflake")
        except Exception as e:
            context.log.warning(f"Summary table not available in Snowflake: {e}")
        
        # Create comprehensive visualization with subplots
        fig = make_subplots(
            rows=3,
            cols=2,
            subplot_titles=[
                "Company Size Distribution",
                "Industry Breakdown", 
                "Top 10 Regions by Company Count",
                "Top 10 Cities by Company Count",
                "Company Era Distribution",
                "Data Quality: Website & LinkedIn Coverage"
            ],
            specs=[
                [{"type": "pie"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Set overall figure layout
        fig.update_layout(
            title_text="French Tech Companies Analysis Dashboard",
            title_font_size=24,
            title_x=0.5,
            height=1200,
            width=1400,
            template="plotly_white",
            showlegend=True
        )
        
        # 1. Company Size Distribution (Pie Chart)
        if 'size_category' in df_companies.columns and df_companies['size_category'].notna().any():
            size_counts = df_companies['size_category'].value_counts()
            fig.add_trace(
                go.Pie(
                    labels=size_counts.index,
                    values=size_counts.values,
                    hole=0.3,
                    marker=dict(colors=px.colors.qualitative.Set3),
                    textinfo="label+percent",
                    textposition="auto",
                    name="Company Size"
                ),
                row=1, col=1
            )
        else:
            # For pie chart subplots, add an empty pie with a text element
            fig.add_trace(
                go.Pie(
                    labels=["No Data"],
                    values=[1],
                    textinfo="text",
                    text=["Company size data<br>not available"],
                    textfont=dict(size=14),
                    marker=dict(colors=["lightgray"]),
                    showlegend=False
                ),
                row=1, col=1
            )
        
        # 2. Industry Breakdown (Horizontal Bar)
        if 'industry' in df_companies.columns and df_companies['industry'].notna().any():
            industry_counts = df_companies['industry'].value_counts()
            fig.add_trace(
                go.Bar(
                    x=industry_counts.values,
                    y=[industry.replace(' & ', ' &<br>').replace(' and ', ' and<br>') for industry in industry_counts.index],
                    orientation='h',
                    marker_color='rgba(55, 128, 191, 0.7)',
                    name="Industries"
                ),
                row=1, col=2
            )
            fig.update_xaxes(title_text="Number of Companies", row=1, col=2)
        
        # 3. Top 10 Regions (Bar Chart)
        if 'region' in df_companies.columns and df_companies['region'].notna().any():
            region_counts = df_companies['region'].value_counts().head(10)
            fig.add_trace(
                go.Bar(
                    x=region_counts.index,
                    y=region_counts.values,
                    marker_color='rgba(219, 64, 82, 0.7)',
                    name="Regions"
                ),
                row=2, col=1
            )
            fig.update_xaxes(title_text="Region", tickangle=45, row=2, col=1)
            fig.update_yaxes(title_text="Number of Companies", row=2, col=1)
        
        # 4. Top 10 Cities (Bar Chart)
        if 'locality' in df_companies.columns and df_companies['locality'].notna().any():
            city_counts = df_companies['locality'].value_counts().head(10)
            fig.add_trace(
                go.Bar(
                    x=city_counts.index,
                    y=city_counts.values,
                    marker_color='rgba(50, 171, 96, 0.7)',
                    name="Cities"
                ),
                row=2, col=2
            )
            fig.update_xaxes(title_text="City", tickangle=45, row=2, col=2)
            fig.update_yaxes(title_text="Number of Companies", row=2, col=2)
        
        # 5. Company Era Distribution (if available)
        if 'company_era' in df_companies.columns and df_companies['company_era'].notna().any():
            era_counts = df_companies['company_era'].value_counts()
            fig.add_trace(
                go.Bar(
                    x=era_counts.index,
                    y=era_counts.values,
                    marker_color='rgba(128, 0, 128, 0.7)',
                    name="Company Eras"
                ),
                row=3, col=1
            )
            fig.update_xaxes(title_text="Company Era", tickangle=45, row=3, col=1)
            fig.update_yaxes(title_text="Number of Companies", row=3, col=1)
        else:
            # Add empty bar chart with message
            fig.add_trace(
                go.Bar(
                    x=["No Data"],
                    y=[0],
                    text=["Company era data\nnot available"],
                    textposition="inside",
                    marker_color='lightgray',
                    name="No Era Data",
                    showlegend=False
                ),
                row=3, col=1
            )
            fig.update_xaxes(title_text="Company Era", row=3, col=1)
            fig.update_yaxes(title_text="Number of Companies", row=3, col=1)
        
        # 6. Data Quality: Website & LinkedIn Coverage
        total_companies = len(df_companies)
        website_count = df_companies['website'].notna().sum() if 'website' in df_companies.columns else 0
        linkedin_count = df_companies['linkedin_url'].notna().sum() if 'linkedin_url' in df_companies.columns else 0
        
        coverage_data = {
            'Metric': ['Companies with Website', 'Companies with LinkedIn', 'Companies without Website', 'Companies without LinkedIn'],
            'Count': [website_count, linkedin_count, total_companies - website_count, total_companies - linkedin_count],
            'Type': ['Has Data', 'Has Data', 'Missing Data', 'Missing Data']
        }
        
        has_data = [website_count, linkedin_count]
        missing_data = [total_companies - website_count, total_companies - linkedin_count]
        
        fig.add_trace(
            go.Bar(
                x=['Website Coverage', 'LinkedIn Coverage'],
                y=has_data,
                name='Has Data',
                marker_color='rgba(26, 118, 255, 0.7)'
            ),
            row=3, col=2
        )
        
        fig.add_trace(
            go.Bar(
                x=['Website Coverage', 'LinkedIn Coverage'],
                y=missing_data,
                name='Missing Data',
                marker_color='rgba(255, 99, 132, 0.7)'
            ),
            row=3, col=2
        )
        
        fig.update_xaxes(title_text="Data Type", row=3, col=2)
        fig.update_yaxes(title_text="Number of Companies", row=3, col=2)
        
        # Add summary statistics as annotations
        stats_text = f"""
        <b>Dataset Overview:</b><br>
        • Total Companies: {total_companies:,}<br>
        • Unique Industries: {df_companies['industry'].nunique() if 'industry' in df_companies.columns else 'N/A'}<br>
        • Unique Regions: {df_companies['region'].nunique() if 'region' in df_companies.columns else 'N/A'}<br>
        • Unique Cities: {df_companies['locality'].nunique() if 'locality' in df_companies.columns else 'N/A'}<br>
        • Website Coverage: {(website_count/total_companies*100):.1f}%<br>
        • LinkedIn Coverage: {(linkedin_count/total_companies*100):.1f}%
        """
        
        fig.add_annotation(
            text=stats_text,
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            align="left",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
            font=dict(size=12)
        )
        
        # Save the interactive HTML report
        save_chart_path = Path(dbt_project.project_dir).parent / "reports" / "french_tech_companies_report.html"
        save_chart_path.parent.mkdir(exist_ok=True)
        
        context.log.info(f"Saving report to: {save_chart_path}")
        fig.write_html(save_chart_path, auto_open=True)
        
        # Tell Dagster about the location of the HTML file
        context.add_output_metadata(
            {"plot_url": dg.MetadataValue.url("file://" + os.fspath(save_chart_path))}
        )
        
        # Log some insights
        context.log.info(f"Report generated successfully with {total_companies} companies analyzed")
        if 'industry' in df_companies.columns:
            top_industry = df_companies['industry'].value_counts().index[0]
            top_industry_count = df_companies['industry'].value_counts().iloc[0]
            context.log.info(f"Top industry: {top_industry} with {top_industry_count} companies")
        
        if 'region' in df_companies.columns:
            top_region = df_companies['region'].value_counts().index[0]
            top_region_count = df_companies['region'].value_counts().iloc[0]
            context.log.info(f"Top region: {top_region} with {top_region_count} companies")
            
    except Exception as e:
        context.log.error(f"Error generating report: {e}")
        raise
    finally:
        # Close Snowflake connection
        if 'snowflake_conn' in locals():
            snowflake_conn.close()
            context.log.info("Closed Snowflake connection")
