# pipelines.py

from tradeindia.items import TradeindiaItem_link,TradeindiaItem_link_final
from tradeindia.db_config import con, cursor, link_table,final_link_table
import logging



class TradeindiaPipeline:

    def open_spider(self, spider):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger.info("Spider opened successfully.")

    def process_item(self, item, spider):
        if isinstance(item, TradeindiaItem_link):
            self.insert_data(item, link_table)
        elif isinstance(item,TradeindiaItem_link_final):
            self.insert_data(item,final_link_table,link_table)
        return item

    def insert_data(self, item, table_name, u_table=None):
        try:
            u_id = item.pop('u_id')
        except:
            u_id=None

        keys = ", ".join(item.keys())
        placeholders = ", ".join(["%s"] * len(item))
        values = tuple(item.values())

        insert_query = f"""
            INSERT IGNORE INTO {table_name} ({keys})
            VALUES ({placeholders})
        """

        try:
            cursor.execute(insert_query, values)
            con.commit()
            self.logger.info("Data inserted successfully.")
        except Exception as e:
            self.logger.error(f"Failed to insert data: {e}")

        # Optional update if u_id is provided
        if u_id:
            try:
                update_query = f"""
                    UPDATE {u_table}
                    SET STATUS = 'Done'
                    WHERE ID = %s
                """
                cursor.execute(update_query, (u_id,))
                con.commit()
                self.logger.info(f"Updated STATUS to 'Done' for ID: {u_id}")
            except Exception as e:
                self.logger.error(f"Failed to update data for ID {u_id}: {e}")
