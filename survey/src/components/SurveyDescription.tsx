import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

export default function SurveyDescription() {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      margin="20px"
    >
      <Card sx={{ width: 450, backgroundColor: "#f3b46c87" }}>
        <CardContent>
          <Typography color="text.secondary" gutterBottom>
            שלום לכולם,
          </Typography>

          <Typography color="text.secondary" gutterBottom>
            במסגרת פרויקט הגמר בתואר הראשון בניהול באוניברסיטת בן גוריון, אנו
            בונות תוכנית עסקית למחלקת האירועים ביקב ׳גלאי׳ הממוקם במושב ניר
            עקיבא.
          </Typography>
          <Typography color="text.secondary" gutterBottom>
            מטעמי נוחות השאלון מנוסח בלשון נקבה אך פונה לשני המינים כאחד.
          </Typography>
          <Typography color="text.secondary" gutterBottom>
            אורכו של השאלון הוא 7 דקות לכל היותר והוא אנונימי לחלוטין.
          </Typography>
          <Typography color="text.secondary" gutterBottom>
            בסיום המענה על הסקר ועם לחיצה על כפתור “לסיום ולהורדת השובר“,
            השובר על סך 40 ש"ח לרשת "ארומה" ירד ישירות למחשב
            וניתן יהיה למצוא אותו בתיקיית ההורדות.
            את השובר ניתן לממש בכל אחד מסניפי הרשת.
          </Typography>
          <Typography color="text.secondary" gutterBottom>
            תודה על ההיענות, דנית ואראלה.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
}